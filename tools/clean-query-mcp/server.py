from __future__ import annotations

import re
from typing import Any

from lab_connectors.mcp import create_mcp_server, guard_timed
from lab_connectors.mcp.errors import McpError, ErrorCode

from catalog import describe_dataset as describe_impl  # noqa: E402
from catalog import get_year_column  # noqa: E402
from catalog import list_datasets as list_impl  # noqa: E402
from catalog import resolve_parquet_path  # noqa: E402
from catalog import search_datasets as search_impl  # noqa: E402
from catalog import load_catalog  # noqa: E402

ALLOWED_FROM = {"clean_input"}
MAX_ROWS_HARD_CAP = 500
BLOCKED_KEYWORDS = {
    "alter",
    "attach",
    "call",
    "copy",
    "create",
    "delete",
    "detach",
    "drop",
    "export",
    "import",
    "insert",
    "install",
    "load",
    "merge",
    "replace",
    "truncate",
    "update",
    "vacuum",
}
TOKEN_RE = re.compile(r"[a-z_][a-z0-9_]*", re.IGNORECASE)


class DuckdbClientError(McpError):
    """Ponte verso lab_connectors.mcp: eredita McpError.

    - code default: QUERY_ERROR (query DuckDB fallite)
    - INVALID_PARAMS: parametri in input invalidi
    - QUERY_SCOPE_VIOLATION: SQL non valida o violate constraint
    """

    def __init__(self, message: str, code: ErrorCode = ErrorCode.QUERY_ERROR) -> None:
        super().__init__(code, message)


def _guard_max_rows(max_rows: int) -> int:
    if max_rows <= 0:
        raise DuckdbClientError("max_rows deve essere maggiore di 0", ErrorCode.INVALID_PARAMS)
    if max_rows > MAX_ROWS_HARD_CAP:
        raise DuckdbClientError(
            f"max_rows oltre il limite hard cap di {MAX_ROWS_HARD_CAP}",
            ErrorCode.INVALID_PARAMS,
        )
    return max_rows


def _validate_select_sql(sql: str) -> str:
    text = (sql or "").strip()
    if not text:
        raise DuckdbClientError("sql vuoto", ErrorCode.INVALID_PARAMS)

    lowered = text.lower()
    if ";" in text:
        raise DuckdbClientError("Query multiple o statement terminati da ';' non consentiti", ErrorCode.QUERY_SCOPE_VIOLATION)
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise DuckdbClientError("Sono consentite solo query SELECT o WITH", ErrorCode.QUERY_SCOPE_VIOLATION)

    scrubbed = re.sub(r"--.*?$", " ", text, flags=re.MULTILINE)
    scrubbed = re.sub(r"/\*.*?\*/", " ", scrubbed, flags=re.DOTALL)
    scrubbed = re.sub(r"'(?:''|[^'])*'", " ", scrubbed)
    scrubbed = re.sub(r'"(?:""|[^"])*"', " ", scrubbed)
    tokens = {token.lower() for token in TOKEN_RE.findall(scrubbed)}

    for keyword in BLOCKED_KEYWORDS:
        if keyword in tokens:
            raise DuckdbClientError(f"Keyword non consentita nella query: {keyword}", ErrorCode.QUERY_SCOPE_VIOLATION)
    return text


# Safe chars for GCS parquet paths: letters, digits, /, _, ., -, :
_SAFE_PATH_RE = re.compile(r"^[a-zA-Z0-9/_.\-:]+$")


def _validate_parquet_paths(paths: list[str]) -> None:
    """Validate parquet paths before building read_parquet expression.

    DuckDB read_parquet with a string path is sensitive to special characters.
    This catches non-ASCII, backslash, and other unsafe chars early with a
    readable error rather than a cryptic DuckDB failure.
    """
    for p in paths:
        if not _SAFE_PATH_RE.match(p):
            raise DuckdbClientError(
                f"Path parquet contiene caratteri non sicuri: '{p}'. "
                f"Caratteri ammessi: lettere, numeri, /, _, ., -, :"
            )


def _duckdb_read(
    dataset: str,
    year: int | None,
    wrapped_sql: str,
    timeout: int = 60,
) -> dict[str, Any]:
    """Helper per esecuzione DuckDB read-only su parquet GCS.

    Estrae e condivide il pattern comune a preview/count/time_series/distinct_values:
    - risoluzione path parquet
    - costruzione source_expr
    - connessione DuckDB in-memory
    - esecuzione con timeout
    - ritorno {columns, rows} o errore
    """
    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"

    # Replace the placeholder in wrapped_sql if present
    sql = wrapped_sql.replace("{SOURCE_EXPR}", source_expr)
    # Inject year filter for single-file multi-year datasets (e.g. giustizia_penale_indicatori)
    if year is not None:
        year_col = get_year_column(dataset)
        if year_col:
            sql = _inject_year_filter(sql, year_col, year)

    from lab_connectors.duckdb import safe_connect
    import concurrent.futures

    with safe_connect(extensions=["httpfs"]) as conn:
        conn.execute("PRAGMA disable_progress_bar")
        conn.execute("SET memory_limit='2GB'")

        def _run():
            result = conn.execute(sql)
            return [item[0] for item in (result.description or [])], result.fetchall()

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(_run)
            columns, rows = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            pool.shutdown(wait=False)
            return {"error": f"Query timeout ({timeout}s). Riduci la complessita o aggiungi filtri."}
        finally:
            pool.shutdown(wait=False)

    return {"columns": columns, "rows": rows}




def _validate_scope(sql: str) -> None:
    """Ensure user SQL only references allowed FROM/JOIN sources (clean_input + local CTEs).

    Blocks read_parquet(...), read_csv(...), direct file paths, and cross-dataset
    FROM/JOIN clauses. CTE aliases defined in the same query are allowed.
    """
    text = (sql or "").strip()

    # Strip string literals to avoid false positives in identifiers.
    scrubbed = re.sub(r"'(?:''|[^'])*'", " '' ", text)
    scrubbed = re.sub(r'"(?:""|[^"])*"', ' "" ', scrubbed)
    scrubbed_lower = scrubbed.lower()

    # Block raw file access patterns.
    if "read_parquet(" in scrubbed_lower:
        raise DuckdbClientError(
            "Accesso diretto a read_parquet() non consentito. "
            "Usa 'FROM clean_input' invece di read_parquet().",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )
    if "read_csv(" in scrubbed_lower:
        raise DuckdbClientError(
            "Accesso diretto a read_csv() non consentito. Usa 'FROM clean_input'.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )

    # Collect CTE names defined in the query.
    cte_name_pattern = re.compile(r"\b([a-z_][a-z0-9_]*)\s+as\s*\(", re.IGNORECASE)
    cte_names: set[str] = set()
    for match in cte_name_pattern.finditer(scrubbed):
        cte_names.add(match.group(1).lower())

    # Extract all FROM <identifier> references.
    from_pattern = re.compile(r"\bfrom\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)
    for match in from_pattern.finditer(scrubbed):
        table_ref = match.group(1).lower()
        if table_ref in ALLOWED_FROM or table_ref in cte_names:
            continue
        raise DuckdbClientError(
            f"Riferimento a tabella non consentito in FROM: '{table_ref}'. "
            f"Solo 'clean_input' e CTE locali sono permessi. "
            f"Usa describe_dataset() per lo schema.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )

    # Extract all JOIN <identifier> references.
    join_pattern = re.compile(r"\bjoin\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)
    for match in join_pattern.finditer(scrubbed):
        table_ref = match.group(1).lower()
        if table_ref in ALLOWED_FROM or table_ref in cte_names:
            continue
        raise DuckdbClientError(
            f"Riferimento a tabella non consentito in JOIN: '{table_ref}'. "
            f"Solo 'clean_input' e CTE locali sono permessi. "
            f"Usa describe_dataset() per lo schema.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )


mcp = create_mcp_server(
    name="clean-query",
    instructions=(
        "MCP server per interrogare i dataset clean del DataCivicLab tramite DuckDB. "
        "Espone catalogo semantico (dataset, colonne, metriche) e esecuzione query read-only. "
        "Il client AI genera il SQL a partire dallo schema."
    ),
)


@mcp.tool(
    description="Lista dei dataset clean disponibili per query.", structured_output=True
)
def list_datasets() -> list[dict[str, Any]]:
    return list_impl()


@mcp.tool(
    description="Cerca nei dataset per nome, descrizione o fonte.",
    structured_output=True,
)
def search_datasets(query: str) -> dict[str, Any]:
    def _exec() -> dict[str, Any]:
        if not (query or "").strip():
            raise DuckdbClientError("query non può essere vuota", ErrorCode.EMPTY_PARAM)
        return {"datasets": search_impl(query.strip()), "query": query.strip()}

    return guard_timed(_exec, "search_datasets")


@mcp.tool(
    description="Descrive lo schema di un dataset: colonne, tipi, ruolo (dimension/metric), periodo.",
    structured_output=True,
)
def describe_dataset(slug: str) -> dict[str, Any]:
    return describe_impl(slug)


def _inject_year_filter(sql: str, year_col: str | None, year: int) -> str:
    """Inietta WHERE {year_col}={year} subito dopo FROM clean_input, prima di GROUP BY/ORDER BY/LIMIT."""
    if not year_col or year is None:
        return sql
    filter_sql = f"WHERE {year_col} = {year}"
    s = sql.strip()
    low = s.lower()

    from_match = list(re.finditer(r'\bfrom\s+clean_input\b', low))
    if not from_match:
        return s

    last_from = from_match[-1].end()
    tail = s[last_from:].strip()

    if tail.lower().startswith("where"):
        return s

    tail_low = tail.lower()
    for keyword in ["group by", "order by", "limit"]:
        idx = tail_low.find(keyword)
        if idx != -1:
            before = tail[:idx].strip()
            after = tail[idx:]
            base = s[:last_from].rstrip()
            if before:
                return f"{base} {before} {filter_sql} {after}".strip()
            return f"{base} {filter_sql} {after}".strip()

    base = s[:last_from].rstrip()
    tail_clean = tail.strip()
    if tail_clean:
        return f"{base} {tail_clean} {filter_sql}".strip()
    return f"{base} {filter_sql}".strip()


@mcp.tool(
    description=(
        "Esegue una query SQL read-only su un dataset clean tramite DuckDB. "
        "Solo SELECT/WITH. Il SQL deve riferire SOLO 'FROM clean_input' o CTE locali. "
        "I path ai parquet sono risolti automaticamente dal catalogo. "
        "Hard cap: max 500 righe, timeout 60s. "
        "Se year è specificato e il dataset ha una colonna anno, la WHERE viene iniettata automaticamente."
    ),
    structured_output=True,
)
def run_query(
    sql: str, dataset: str, max_rows: int = 100, year: int | None = None
) -> dict[str, Any]:
    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_scope(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    try:
        _validate_select_sql(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    if year is not None:
        year_col = get_year_column(dataset)
        if year_col:
            sql = _inject_year_filter(sql, year_col, year)

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return {"error": str(exc)}
    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"
    wrapped_sql = (
        f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) "
        f"SELECT * FROM ({sql}) AS q LIMIT {max_rows + 1}"
    )

    def _exec() -> dict[str, Any]:
        _guard_max_rows(max_rows)

        from lab_connectors.duckdb import safe_connect
        import concurrent.futures

        with safe_connect(extensions=["httpfs"]) as conn:
            conn.execute("PRAGMA disable_progress_bar")
            conn.execute("SET memory_limit='2GB'")

            def _run_query():
                result = conn.execute(wrapped_sql)
                columns = [item[0] for item in (result.description or [])]
                rows_raw = result.fetchall()
                return columns, rows_raw

            # 60s hard timeout: ThreadPoolExecutor without 'with' so we don't
            # wait for the worker to finish after timeout. The orphan thread will
            # eventually finish and its connection is isolated (in-memory).
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(_run_query)
                columns, rows_raw = future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                return {
                    "error": "Query timeout (60s). Ridurre la complessita o aggiungere filtri."
                }
            finally:
                pool.shutdown(wait=False)

        truncated = len(rows_raw) > max_rows
        rows = rows_raw[:max_rows]
        return {
            "columns": columns,
            "rows": [list(row) for row in rows],
            "row_count": len(rows),
            "truncated": truncated,
            "dataset": dataset,
        }

    return guard_timed(_exec, "run_query")


@mcp.tool(
    description="Restituisce statistiche sulla cache GCS del catalogo (utile per debug).",
    structured_output=True,
)
def cache_stats() -> dict[str, Any]:
    from catalog import gcs_cache_stats

    return gcs_cache_stats()



@mcp.tool(
    description=(
        "Helper per aggregazioni pre-scritte: somma una metrica raggruppando per una o più dimensioni. "
        "Restituisce SQL che può essere passato a run_query(). "
        "metric: colonna numerica da sommare (es. 'numero_pensioni'). "
        "group_by: lista di dimensioni (es. ['anno','regione']). "
        "filters:WHERE aggiuntivo opzionale (es. \"anno = 2023 AND regione = 'Lombardia'\")."
    ),
    structured_output=True,
)
def aggregate(
    dataset: str,
    metric: str,
    group_by: list[str],
    filters: str | None = None,
    year: int | None = None,
) -> dict[str, Any]:
    if not metric:
        return {"error": "metric non può essere vuota"}
    if not group_by:
        return {"error": "group_by deve avere almeno una dimensione"}

    schema = describe_impl(dataset)
    if "error" in schema:
        return schema
    col_names = {c["name"] for c in schema.get("columns", [])}
    for col in group_by:
        if col not in col_names:
            return {"error": f"Colonna group_by '{col}' non trovata. Disponibili: {', '.join(sorted(col_names))}"}
    if metric not in col_names:
        return {"error": f"Metrica '{metric}' non trovata. Disponibili: {', '.join(sorted(col_names))}"}

    year_col = get_year_column(dataset)
    where_parts = []
    if year is not None and year_col:
        where_parts.append(f"{year_col} = {year}")
    if filters:
        where_parts.append(f"({filters})")
    where_clause = ""
    if where_parts:
        where_clause = "WHERE " + " AND ".join(where_parts)

    group_cols = ", ".join(group_by)
    sql = (
        f"SELECT {group_cols}, SUM({metric}) AS total "
        f"FROM clean_input {where_clause} "
        f"GROUP BY {group_cols} "
        f"ORDER BY {group_by[0]}, total DESC"
    )
    return {
        "sql": sql,
        "dataset": dataset,
        "metric": metric,
        "group_by": group_by,
        "year": year,
        "note": "Passa questo sql a run_query(). Non include LIMIT; aggiungilo in run_query.",
    }


@mcp.tool(
    description=(
        "Anteprima: prime N righe di un dataset senza SQL. "
        "Utile per esplorare la struttura prima di scrivere una query. "
        "Non usa SQL, ritorna righe raw dal parquet."
    ),
    structured_output=True,
)
def preview(dataset: str, limit: int = 10, year: int | None = None) -> dict[str, Any]:
    if limit <= 0 or limit > MAX_ROWS_HARD_CAP:
        return {"error": f"limit deve essere tra 1 e {MAX_ROWS_HARD_CAP}"}
    wrapped_sql = (
        f"WITH clean_input AS (SELECT * FROM read_parquet({{SOURCE_EXPR}})) "
        f"SELECT * FROM clean_input LIMIT {limit}"
    )
    result = _duckdb_read(dataset, year, wrapped_sql)
    if "error" in result:
        return result
    return {
        "columns": result["columns"],
        "rows": [list(row) for row in result["rows"]],
        "row_count": len(result["rows"]),
        "dataset": dataset,
        "limit_applied": limit,
    }


@mcp.tool(
    description=(
        "Conteggio righe: numero totale di record in un dataset, opzionalmente filtrato per anno. "
        "Utile per verificare copertura e dimensionalità prima di query complesse."
    ),
    structured_output=True,
)
def count(dataset: str, year: int | None = None) -> dict[str, Any]:
    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"

    wrapped_sql = f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) SELECT COUNT(*) AS total FROM clean_input"
    if year is not None:
        year_col = get_year_column(dataset)
        if year_col:
            wrapped_sql = _inject_year_filter(wrapped_sql, year_col, year)

    def _exec() -> dict[str, Any]:
        from lab_connectors.duckdb import safe_connect
        import concurrent.futures

        with safe_connect(extensions=["httpfs"]) as conn:
            conn.execute("PRAGMA disable_progress_bar")
            conn.execute("SET memory_limit='2GB'")

            def _run():
                result = conn.execute(wrapped_sql)
                return result.fetchone()[0]

            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(_run)
                total = future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                pool.shutdown(wait=False)
                return {"error": "Query timeout (60s). Riduci la complessita o aggiungi filtri."}
            finally:
                pool.shutdown(wait=False)

        return {
            "dataset": dataset,
            "total_rows": total,
            "year_filter": year,
            "files_count": len(parquet_paths),
        }

    return guard_timed(_exec, "count")


@mcp.tool(
    description=(
        "Serie storica: valori di una metrica nel tempo, raggruppati per una dimensione (es. regione). "
        "Se year è specificato, ritorna una singola annualità. "
        "Se year è None, ritorna tutti gli anni disponibili con la metrica aggregata per la dimensione scelta."
    ),
    structured_output=True,
)
def time_series(
    dataset: str,
    metric: str,
    group_by: str,
    year: int | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    if limit <= 0 or limit > MAX_ROWS_HARD_CAP:
        return {"error": f"limit deve essere tra 1 e {MAX_ROWS_HARD_CAP}"}
    schema = describe_impl(dataset)
    if "error" in schema:
        return schema

    col_names = {c["name"] for c in schema.get("columns", [])}
    if metric not in col_names:
        return {"error": f"Metrica '{metric}' non trovata. Disponibili: {', '.join(sorted(col_names))}"}
    if group_by not in col_names:
        return {"error": f"Dimensione group_by '{group_by}' non trovata. Disponibili: {', '.join(sorted(col_names))}"}

    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"

    year_col = get_year_column(dataset)
    if year_col is None:
        return {"error": f"Dataset '{dataset}' non ha una colonna anno riconosciuta. Impossibile costruire serie storica."}

    select_cols = f"{year_col}, {group_by}"
    group_cols = f"{year_col}, {group_by}"
    order_clause = f"{year_col}, {group_by}"

    wrapped_sql = (
        f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) "
        f"SELECT {select_cols}, SUM({metric}) AS value "
        f"FROM clean_input "
        f"GROUP BY {group_cols} "
        f"ORDER BY {order_clause} "
        f"LIMIT {limit + 1}"
    )
    if year is not None:
        wrapped_sql = _inject_year_filter(wrapped_sql, year_col, year)

    def _exec() -> dict[str, Any]:
        from lab_connectors.duckdb import safe_connect
        import concurrent.futures

        with safe_connect(extensions=["httpfs"]) as conn:
            conn.execute("PRAGMA disable_progress_bar")
            conn.execute("SET memory_limit='2GB'")

            def _run():
                result = conn.execute(wrapped_sql)
                return [item[0] for item in (result.description or [])], result.fetchall()

            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(_run)
                columns, rows = future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                pool.shutdown(wait=False)
                return {"error": "Query timeout (60s). Riduci la complessita o aggiungi filtri."}
            finally:
                pool.shutdown(wait=False)

        truncated = len(rows) > limit
        return {
            "columns": columns,
            "rows": [list(row) for row in rows[:limit]],
            "row_count": len(rows),
            "truncated": truncated,
            "dataset": dataset,
            "metric": metric,
            "group_by": group_by,
            "year_filter": year,
        }

    return guard_timed(_exec, "time_series")


@mcp.tool(
    description=(
        "Valori distinti di una colonna. "
        "Utile per popolare dropdown/filter nelle UI, o per verificare i valori disponibili prima di query."
    ),
    structured_output=True,
)
def distinct_values(dataset: str, column: str, limit: int = 100) -> dict[str, Any]:
    if limit <= 0 or limit > MAX_ROWS_HARD_CAP:
        return {"error": f"limit deve essere tra 1 e {MAX_ROWS_HARD_CAP}"}
    schema = describe_impl(dataset)
    if "error" in schema:
        return schema

    col_names = {c["name"] for c in schema.get("columns", [])}
    if column not in col_names:
        return {"error": f"Colonna '{column}' non trovata. Disponibili: {', '.join(sorted(col_names))}"}

    try:
        parquet_paths = resolve_parquet_path(dataset, year=None)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"

    wrapped_sql = (
        f"WITH clean_input AS (SELECT {column} FROM read_parquet({source_expr})) "
        f"SELECT DISTINCT {column} FROM clean_input WHERE {column} IS NOT NULL LIMIT {limit + 1}"
    )

    def _exec() -> dict[str, Any]:
        from lab_connectors.duckdb import safe_connect
        import concurrent.futures

        with safe_connect(extensions=["httpfs"]) as conn:
            conn.execute("PRAGMA disable_progress_bar")
            conn.execute("SET memory_limit='2GB'")

            def _run():
                result = conn.execute(wrapped_sql)
                return [item[0] for item in (result.description or [])], result.fetchall()

            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(_run)
                columns, rows = future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                pool.shutdown(wait=False)
                return {"error": "Query timeout (60s). Riduci la complessita o aggiungi filtri."}
            finally:
                pool.shutdown(wait=False)

        truncated = len(rows) > limit
        return {
            "column": column,
            "values": [row[0] for row in rows[:limit]],
            "count": len(rows),
            "truncated": truncated,
            "dataset": dataset,
        }

    return guard_timed(_exec, "distinct_values")


@mcp.tool(
    description=(
        "Cerca dataset che abbiano una colonna di tipo 'metric' (numerica). "
        "Filtra per nome colonna o pattern, e ritorna il catalogo dei match con schema resumí."
    ),
    structured_output=True,
)
def find_metric_datasets(query: str = "", metric_name: str = "", limit: int = 20) -> dict[str, Any]:
    def _exec() -> dict[str, Any]:
        catalog = load_catalog()
        results = []
        for ds in catalog:
            cols = ds.get("columns", [])
            metric_cols = [
                {"name": c["name"], "type": c.get("type"), "description": c.get("description")}
                for c in cols
                if c.get("role") == "metric"
            ]
            if not metric_cols:
                continue

            # Filter by query (search in name/description/source)
            q_lower = query.lower()
            if q_lower and q_lower not in ds.get("name", "").lower() and q_lower not in ds.get("description", "").lower() and q_lower not in ds.get("source", "").lower():
                continue

            # Filter by metric name
            if metric_name:
                mn_lower = metric_name.lower()
                if not any(mn_lower in mc["name"].lower() for mc in metric_cols):
                    continue

            results.append({
                "slug": ds["slug"],
                "name": ds["name"],
                "source": ds.get("source"),
                "period": ds.get("period"),
                "metric_columns": metric_cols,
                "match_hint": metric_name or query,
            })

            if len(results) >= limit:
                break

        return {
            "datasets": results,
            "count": len(results),
            "query": query,
            "metric_name": metric_name,
            "note": "Ritorna dataset che hanno colonne role=metric. Usa describe_dataset per lo schema completo.",
        }

    return guard_timed(_exec, "find_metric_datasets")


@mcp.tool(
    description=(
        "Cerca dataset per nome o descrizione di colonna. "
        "Cerca sia nelle meta dataset (nome, descrizione, source) che nei nomi colonna."
    ),
    structured_output=True,
)
def column_search(query: str, limit: int = 15) -> dict[str, Any]:
    def _exec() -> dict[str, Any]:
        catalog = load_catalog()
        q = query.lower()
        results = []
        for ds in catalog:
            matched_cols = []
            for col in ds.get("columns", []):
                if q in col.get("name", "").lower() or q in col.get("description", "").lower():
                    matched_cols.append({
                        "name": col["name"],
                        "type": col.get("type"),
                        "role": col.get("role"),
                        "description": col.get("description"),
                    })

            # Match in dataset metadata or in column names/descriptions
            meta_match = q in ds.get("name", "").lower() or q in ds.get("description", "").lower()

            if matched_cols or meta_match:
                results.append({
                    "slug": ds["slug"],
                    "name": ds["name"],
                    "source": ds.get("source"),
                    "period": ds.get("period"),
                    "matched_columns": matched_cols,
                    "meta_match": meta_match,
                })

            if len(results) >= limit:
                break

        return {
            "datasets": results,
            "count": len(results),
            "query": query,
            "note": "Meta_match=True indica match su nome/descrizione dataset; matched_columns indica match su colonna.",
        }

    return guard_timed(_exec, "column_search")


@mcp.tool(
    description=(
        "Pre-check di una query SQL: valida scope, sintassi e riferimenti a clean_input. "
        "Non esegue la query — usa EXPLAIN di DuckDB per validazione semantica base. "
        "Usa preview() per un campione reale dei dati."
    ),
    structured_output=True,
)
def explain_query(sql: str, dataset: str) -> dict[str, Any]:
    try:
        parquet_paths = resolve_parquet_path(dataset, year=None)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    try:
        _validate_scope(sql)
    except DuckdbClientError as exc:
        return {"validation_error": str(exc), "valid": False}

    try:
        _validate_select_sql(sql)
    except DuckdbClientError as exc:
        return {"validation_error": str(exc), "valid": False}

    # Validate with actual DuckDB EXPLAIN on the wrapped query
    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"
    wrapped_sql = f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) {sql}"

    def _exec() -> dict[str, Any]:
        from lab_connectors.duckdb import safe_connect
        import concurrent.futures

        with safe_connect(extensions=["httpfs"]) as conn:
            conn.execute("PRAGMA disable_progress_bar")
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = pool.submit(lambda: conn.execute(f"EXPLAIN {wrapped_sql}"))
                explain_result = future.result(timeout=30)
                row = explain_result.fetchone() if explain_result else None
                plan_text = row[1] if row and len(row) > 1 else (row[0] if row else None)
            finally:
                pool.shutdown(wait=False)

        return {
            "valid": True,
            "dataset": dataset,
            "sql": sql,
            "source_parquets": parquet_paths,
            "plan_excerpt": plan_text[:200] if plan_text else None,
            "note": "EXPLAIN eseguito con successo — query sintatticamente e semanticamente valida.",
            "tip": "Usa preview() per verificare i dati reali prima di run_query().",
        }

    return guard_timed(_exec, "explain_query")


if __name__ == "__main__":
    mcp.run()
