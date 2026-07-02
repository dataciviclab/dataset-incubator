from __future__ import annotations

import json as _json
import re
from pathlib import Path as _Path
from typing import Any

from lab_connectors.mcp import create_mcp_server, guard_timed
from lab_connectors.mcp.errors import McpError, ErrorCode
from lab_connectors.mcp.cache import TtlCache

from .catalog import describe_dataset as describe_impl  # noqa: E402
from .catalog import get_year_column  # noqa: E402
from .catalog import list_datasets as list_impl  # noqa: E402
from .catalog import resolve_parquet_path  # noqa: E402
from .catalog import search_datasets as search_impl  # noqa: E402
from .catalog import load_catalog  # noqa: E402

# Path assoluto alla relationship map (generata da build_relationship_map.py)
_RELATIONSHIP_MAP_PATH = _Path(__file__).resolve().parents[2] / "registry" / "relationship_map.json"

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

# Cache risultati query: TTL 120s per dataset_overview e COUNT frequenti
_query_cache: TtlCache[tuple, dict] = TtlCache(ttl_seconds=120)


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
        raise DuckdbClientError(
            "Query multiple o statement terminati da ';' non consentiti",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise DuckdbClientError(
            "Sono consentite solo query SELECT o WITH", ErrorCode.QUERY_SCOPE_VIOLATION
        )

    scrubbed = re.sub(r"--.*?$", " ", text, flags=re.MULTILINE)
    scrubbed = re.sub(r"/\*.*?\*/", " ", scrubbed, flags=re.DOTALL)
    scrubbed = re.sub(r"'(?:''|[^'])*'", " ", scrubbed)
    scrubbed = re.sub(r'"(?:""|[^"])*"', " ", scrubbed)
    tokens = {token.lower() for token in TOKEN_RE.findall(scrubbed)}

    for keyword in BLOCKED_KEYWORDS:
        if keyword in tokens:
            raise DuckdbClientError(
                f"Keyword non consentita nella query: {keyword}", ErrorCode.QUERY_SCOPE_VIOLATION
            )
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


def _execute_sql(
    dataset: str,
    sql: str,
    year: int | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Helper DuckDB: risolve path, connette, esegue, ritorna {columns, rows}.

    Il parametro ``sql`` è il corpo della query che usa ``clean_input`` come FROM.
    La CTE ``clean_input`` viene costruita automaticamente.
    Il filtro anno NON viene iniettato qui — i chiamanti devono applicarlo
    PRIMA del wrapping se necessario (es. run_query inietta prima di avvolgere).
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

    wrapped_sql = f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) {sql}"

    from lab_connectors.duckdb import gcs_connect
    import concurrent.futures

    with gcs_connect(parquet_paths[0]) as conn:

        def _run():
            result = conn.execute(wrapped_sql)
            return [item[0] for item in (result.description or [])], result.fetchall()

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(_run)
            columns, rows = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            pool.shutdown(wait=False)
            return {
                "error": f"Query timeout ({timeout}s). Riduci la complessita o aggiungi filtri."
            }
        finally:
            pool.shutdown(wait=False)

    return {"columns": columns, "rows": rows}


def _execute_sql_batch(
    dataset: str,
    sql_list: list[str],
    year: int | None = None,
    timeout: int = 60,
) -> list[dict[str, Any]]:
    """Esegue più query SQL nella stessa connessione DuckDB.

    Utile per tool che devono fare più query sullo stesso dataset
    (es. dataset_overview: count + preview) senza ripetere connessione GCS.
    """
    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return [{"error": str(exc)}] * len(sql_list)

    try:
        _validate_parquet_paths(parquet_paths)
    except DuckdbClientError as exc:
        return [{"error": str(exc)}] * len(sql_list)

    escaped_paths = "', '".join(p.replace("'", "''") for p in parquet_paths)
    if len(parquet_paths) == 1:
        source_expr = f"'{escaped_paths}'"
    else:
        source_expr = f"['{escaped_paths}']"

    from lab_connectors.duckdb import gcs_connect
    import concurrent.futures

    with gcs_connect(parquet_paths[0]) as conn:

        def _run_all():
            batch_results: list[dict[str, Any]] = []
            for sql in sql_list:
                wrapped = f"WITH clean_input AS (SELECT * FROM read_parquet({source_expr})) {sql}"
                result = conn.execute(wrapped)
                cols = [item[0] for item in (result.description or [])]
                rows = result.fetchall()
                batch_results.append({"columns": cols, "rows": rows})
            return batch_results

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(_run_all)
            batch_results = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            pool.shutdown(wait=False)
            return [{"error": f"Query timeout ({timeout}s)."}] * len(sql_list)
        finally:
            pool.shutdown(wait=False)

    return batch_results


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


# ── Cross-dataset query ───────────────────────────────────────────────────────


def _validate_cross_scope(sql: str, allowed_tables: set[str]) -> None:
    """Come _validate_scope, ma permette riferimenti a tabelle in allowed_tables.

    allowed_tables: set di nomi di dataset che la query può referenziare
                    nei FROM/JOIN (oltre a CTE locali).
    """
    text = (sql or "").strip()

    scrubbed = re.sub(r"'(?:''|[^'])*'", " '' ", text)
    scrubbed = re.sub(r'"(?:""|[^"])*"', ' "" ', scrubbed)
    scrubbed_lower = scrubbed.lower()

    if "read_parquet(" in scrubbed_lower:
        raise DuckdbClientError(
            "Accesso diretto a read_parquet() non consentito. "
            "Usa i nomi dei dataset passati in 'datasets'.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )
    if "read_csv(" in scrubbed_lower:
        raise DuckdbClientError(
            "Accesso diretto a read_csv() non consentito.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )

    # CTE names defined in the query
    cte_name_pattern = re.compile(r"\b([a-z_][a-z0-9_]*)\s+as\s*\(", re.IGNORECASE)
    cte_names: set[str] = set()
    for match in cte_name_pattern.finditer(scrubbed):
        cte_names.add(match.group(1).lower())

    # allowed: ALLOWED_FROM + CTE locali + dataset names
    allowed = ALLOWED_FROM | cte_names | allowed_tables

    # DuckDB permette FROM 'url.parquet' (string literal come tabella).
    # Le stringhe originali sono già state sostituite con '' dalla scrub,
    # quindi cerchiamo FROM '' o JOIN ''.
    if re.search(r"\bfrom\s+''", scrubbed_lower):
        raise DuckdbClientError(
            "Accesso diretto a file parquet via FROM '...' non consentito. "
            "Usa i nomi dei dataset passati in 'datasets'.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )
    if re.search(r"\bjoin\s+''", scrubbed_lower):
        raise DuckdbClientError(
            "Accesso diretto a file parquet via JOIN '...' non consentito. "
            "Usa i nomi dei dataset passati in 'datasets'.",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )

    # Check FROM references (identificatori)
    from_pattern = re.compile(r"\bfrom\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)
    for match in from_pattern.finditer(scrubbed):
        table_ref = match.group(1).lower()
        if table_ref in allowed:
            continue
        raise DuckdbClientError(
            f"Riferimento a tabella non consentito in FROM: '{table_ref}'. "
            f"Usa i nomi dei dataset passati in 'datasets': "
            f"{', '.join(sorted(allowed_tables))}",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )

    # Check JOIN references (identificatori)
    join_pattern = re.compile(r"\bjoin\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)
    for match in join_pattern.finditer(scrubbed):
        table_ref = match.group(1).lower()
        if table_ref in allowed:
            continue
        raise DuckdbClientError(
            f"Riferimento a tabella non consentito in JOIN: '{table_ref}'. "
            f"Usa i nomi dei dataset passati in 'datasets': "
            f"{', '.join(sorted(allowed_tables))}",
            ErrorCode.QUERY_SCOPE_VIOLATION,
        )


def _execute_cross_sql(
    datasets: list[str],
    sql: str,
    timeout: int = 60,
) -> dict[str, Any]:
    """Helper per query su più dataset. Costruisce CTE multi-tabella."""
    from lab_connectors.duckdb import safe_connect

    # Risolvi path per ogni dataset
    cte_defs: list[str] = []
    for slug in datasets:
        try:
            paths = resolve_parquet_path(slug, year=None)
        except (ValueError, FileNotFoundError) as exc:
            return {"error": f"Path per '{slug}' non trovato: {exc}"}

        if not paths:
            return {"error": f"Nessun parquet trovato per '{slug}'"}

        # HTTPS per evitare bug httpfs
        https_paths = []
        for p in paths:
            if p.startswith("s3://"):
                p = f"https://storage.googleapis.com/{p[5:]}"
            https_paths.append(p)

        escaped = "', '".join(p.replace("'", "''") for p in https_paths)
        array_expr = f"['{escaped}']" if len(https_paths) > 1 else f"'{escaped}'"
        cte_defs.append(f"{slug} AS (SELECT * FROM read_parquet({array_expr}))")

    cte_sql = ", ".join(cte_defs)
    wrapped_sql = f"WITH {cte_sql} {sql}"

    allowed_tables = set(datasets)

    # Scope validation: permette riferimenti ai dataset richiesti
    try:
        _validate_cross_scope(sql, allowed_tables)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    try:
        _validate_select_sql(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    with safe_connect() as conn:
        try:
            result = conn.execute(wrapped_sql)
            columns = [item[0] for item in (result.description or [])]
            rows = result.fetchall()
        except Exception as exc:
            return {"error": f"Errore cross query: {exc}"}

    return {"columns": columns, "rows": rows}


mcp = create_mcp_server(
    name="clean-query",
    instructions=(
        "MCP server per interrogare i dataset clean del DataCivicLab tramite DuckDB. "
        "Espone catalogo semantico (dataset, colonne, metriche) e esecuzione query read-only. "
        "Il client AI genera il SQL a partire dallo schema."
    ),
)


@mcp.tool(
    description=(
        "Esegue una query SQL che incrocia PIU' dataset clean. "
        "I dataset specificati in 'datasets' diventano tabelle utilizzabili "
        "nei FROM/JOIN della query. "
        "Esempio: cross_query(datasets=['irpef_comunale','popolazione_istat_comunale_2019_2025'], "
        'sql="SELECT i.denominazione_comune, i.reddito_imponibile_eur, p.popolazione_residente '
        "FROM irpef_comunale i JOIN popolazione_istat_comunale_2019_2025 p "
        "ON i.codice_istat_comune = p.codice_comune WHERE p.comune = 'Milano'\")"
    ),
    structured_output=True,
)
def cross_query(
    datasets: list[str],
    sql: str,
    max_rows: int = 100,
) -> dict[str, Any]:
    """Esegue una query su più dataset.

    Args:
        datasets: Lista di slug di dataset (es. ['irpef_comunale', 'popolazione_istat_comunale_2019_2025']).
        sql: SQL da eseguire. I dataset sono referenziabili per nome.
        max_rows: Max righe da restituire (default 100, hard cap 500).

    Returns:
        {columns, rows, row_count, truncated, datasets}
    """
    if not datasets or len(datasets) < 2:
        return {
            "error": "cross_query richiede almeno 2 dataset. Usa run_query per singolo dataset."
        }

    max_rows = _guard_max_rows(max_rows)
    capped_sql = f"SELECT * FROM ({sql}) AS q LIMIT {max_rows + 1}"

    def _exec() -> dict[str, Any]:
        result = _execute_cross_sql(datasets, capped_sql)
        if "error" in result:
            return result
        rows_raw = result["rows"]
        truncated = len(rows_raw) > max_rows
        rows = rows_raw[:max_rows]
        return {
            "columns": result["columns"],
            "rows": [list(row) for row in rows],
            "row_count": len(rows),
            "truncated": truncated,
            "datasets": datasets,
        }

    return guard_timed(_exec, "cross_query")


@mcp.tool(description="Lista dei dataset clean disponibili per query.", structured_output=True)
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

    from_match = list(re.finditer(r"\bfrom\s+clean_input\b", low))
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
        _validate_scope(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    try:
        _validate_select_sql(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    _guard_max_rows(max_rows)

    # Inietta year filter PRIMA del wrapping, così WHERE opera su clean_input
    # e non sulla subquery esterna (evita "Column anno not found in FROM clause")
    sql_to_exec = sql
    if year is not None:
        year_col = get_year_column(dataset)
        if year_col:
            sql_to_exec = _inject_year_filter(sql_to_exec, year_col, year)

    wrapped_sql = f"SELECT * FROM ({sql_to_exec}) AS q LIMIT {max_rows + 1}"

    def _exec() -> dict[str, Any]:
        result = _execute_sql(dataset, wrapped_sql, year=year)
        if "error" in result:
            return result
        rows_raw = result["rows"]
        truncated = len(rows_raw) > max_rows
        rows = rows_raw[:max_rows]
        return {
            "columns": result["columns"],
            "rows": [list(row) for row in rows],
            "row_count": len(rows),
            "truncated": truncated,
            "dataset": dataset,
        }

    return guard_timed(_exec, "run_query")


@mcp.tool(
    description=(
        "Restituisce statistiche sulle cache: GCS path resolution e risultati query. "
        "Utile per monitorare efficienza cache e debug."
    ),
    structured_output=True,
)
def cache_stats() -> dict[str, Any]:
    from .catalog import gcs_cache_stats

    gcs_stats = gcs_cache_stats()
    query_stats = _query_cache.stats

    return {
        "gcs_path_resolution": gcs_stats,
        "query_results": {
            "entries": query_stats.entries,
            "oldest_age_seconds": round(query_stats.oldest_age_seconds, 1),
            "ttl_seconds": query_stats.ttl_seconds,
        },
        "note": "query_results cache: dataset_overview e COUNT frequenti, TTL 120s",
    }


@mcp.tool(
    description=(
        "Panoramica completa di un dataset: schema + conteggio righe + anteprima dati. "
        "Combina describe_dataset, count e preview in una singola chiamata. "
        "Usa una sola connessione DuckDB per count e preview, riducendo la latenza. "
        "Utile per esplorare rapidamente un dataset prima di scrivere query SQL. "
        "I risultati sono cacheati per 120s."
    ),
    structured_output=True,
)
def dataset_overview(slug: str, limit: int = 10) -> dict[str, Any]:
    if limit <= 0 or limit > MAX_ROWS_HARD_CAP:
        return {"error": f"limit deve essere tra 1 e {MAX_ROWS_HARD_CAP}"}

    # Cache check
    cache_key = ("dataset_overview", slug, limit)
    cached = _query_cache.get(cache_key)
    if cached is not None:
        return cached

    schema = describe_impl(slug)
    if "error" in schema:
        return schema

    def _exec() -> dict[str, Any]:
        # Due query nella stessa connessione: COUNT + preview
        sql_list = [
            "SELECT COUNT(*) AS total FROM clean_input",
            f"SELECT * FROM clean_input LIMIT {limit}",
        ]
        batch = _execute_sql_batch(slug, sql_list)
        if "error" in batch[0]:
            return {**schema, "error": batch[0]["error"]}

        total_rows = batch[0]["rows"][0][0] if batch[0]["rows"] else 0
        preview_cols = batch[1]["columns"]
        preview_rows = batch[1]["rows"]

        result = {
            "slug": slug,
            "name": schema.get("name"),
            "description": schema.get("description"),
            "source": schema.get("source"),
            "period": schema.get("period"),
            "columns": schema.get("columns", []),
            "total_rows": total_rows,
            "preview": {
                "columns": preview_cols,
                "rows": [list(row) for row in preview_rows],
                "row_count": len(preview_rows),
                "limit_applied": limit,
            },
            "_cached": False,
        }
        _query_cache.set(cache_key, result)
        return result

    return guard_timed(_exec, "dataset_overview")


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
            if (
                q_lower
                and q_lower not in ds.get("name", "").lower()
                and q_lower not in ds.get("description", "").lower()
                and q_lower not in ds.get("source", "").lower()
            ):
                continue

            # Filter by metric name
            if metric_name:
                mn_lower = metric_name.lower()
                if not any(mn_lower in mc["name"].lower() for mc in metric_cols):
                    continue

            results.append(
                {
                    "slug": ds["slug"],
                    "name": ds["name"],
                    "source": ds.get("source"),
                    "period": ds.get("period"),
                    "metric_columns": metric_cols,
                    "match_hint": metric_name or query,
                }
            )

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
                    matched_cols.append(
                        {
                            "name": col["name"],
                            "type": col.get("type"),
                            "role": col.get("role"),
                            "description": col.get("description"),
                        }
                    )

            # Match in dataset metadata or in column names/descriptions
            meta_match = q in ds.get("name", "").lower() or q in ds.get("description", "").lower()

            if matched_cols or meta_match:
                results.append(
                    {
                        "slug": ds["slug"],
                        "name": ds["name"],
                        "source": ds.get("source"),
                        "period": ds.get("period"),
                        "matched_columns": matched_cols,
                        "meta_match": meta_match,
                    }
                )

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
        from lab_connectors.duckdb import gcs_connect
        import concurrent.futures

        with gcs_connect(parquet_paths[0]) as conn:
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


# ── Relationship Map ──────────────────────────────────────────────────────────


def _load_relationship_map() -> dict[str, Any]:
    """Carica relationship_map.json (generato da build_relationship_map.py)."""
    try:
        return _json.loads(_RELATIONSHIP_MAP_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, _json.JSONDecodeError) as exc:
        return {"error": f"relationship_map.json non trovato o corrotto: {exc}"}


@mcp.tool(
    description=(
        "Mostra la mappa delle relazioni tra dataset del Lab. "
        "Ogni dataset si collega a un registro anagrafico (comuni_master, bdap_anagrafe_enti) "
        "tramite una chiave (codice_istat, denominazione, ...). "
        "Filtra per chiave, dataset o registro per esplorare le connessioni."
    ),
    structured_output=True,
)
def dataset_graph(
    by_key: str = "",
    by_dataset: str = "",
    by_registry: str = "",
) -> dict[str, Any]:
    """Esplora la mappa delle relazioni tra dataset.

    Args:
        by_key: Filtra per chiave (es. 'codice_istat', 'denominazione').
        by_dataset: Filtra per dataset slug (es. 'irpef_comunale').
        by_registry: Filtra per registro (es. 'comuni_master').

    Returns:
        Dict con le relazioni trovate, o l'intera mappa se nessun filtro.
    """

    def _exec() -> dict[str, Any]:
        graph = _load_relationship_map()
        if "error" in graph:
            return graph

        result: dict[str, Any] = {
            "description": graph.get("description"),
            "hub_hint": graph.get("hub_hint"),
            "registries": {},
        }

        # Filtra per registro
        registries_to_show = graph.get("registries", {})
        if by_registry:
            reg = registries_to_show.get(by_registry)
            if reg:
                registries_to_show = {by_registry: reg}
            else:
                return {
                    "error": f"Registro '{by_registry}' non trovato. Disponibili: {list(registries_to_show.keys())}"
                }

        for reg_name, reg_data in registries_to_show.items():
            keys_filtered = {}
            for key_name, key_data in reg_data.get("keys", {}).items():
                # Filtra per chiave — se specificata, mostra solo quella
                if by_key and by_key.lower() not in key_name.lower():
                    continue

                # Filtra dataset
                datasets = key_data.get("datasets", [])
                if by_dataset:
                    datasets = [
                        d
                        for d in datasets
                        if by_dataset.lower() in d["slug"].lower()
                        or by_dataset.lower() in d["name"].lower()
                    ]

                if not datasets:
                    continue

                keys_filtered[key_name] = {
                    "description": key_data["description"],
                    "datasets": datasets,
                }

            if keys_filtered:
                result["registries"][reg_name] = {
                    "description": reg_data.get("description", ""),
                    "keys": keys_filtered,
                }

        # Conta
        n_keys = sum(len(r["keys"]) for r in result["registries"].values())
        n_ds = sum(
            len(k["datasets"]) for r in result["registries"].values() for k in r["keys"].values()
        )

        result["summary"] = {
            "keys": n_keys,
            "datasets": n_ds,
            "registries": len(result["registries"]),
        }

        # Suggerimenti se nessun filtro
        if not by_key and not by_dataset and not by_registry:
            result["tip"] = (
                "Usa by_key='codice_istat' per vedere tutti i dataset collegati via ISTAT, "
                "by_dataset='irpef_comunale' per vedere come si collega, "
                "o by_registry='comuni_master' per esplorare un registro."
            )
            # Mostra anche i non collegati
            result["unconnected_datasets"] = graph.get("unconnected_datasets", [])

        return result

    return guard_timed(_exec, "dataset_graph")


def main() -> None:
    """Entry point per l'MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
