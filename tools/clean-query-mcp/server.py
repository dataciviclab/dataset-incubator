from __future__ import annotations

import re
from typing import Any

from mcp.server.fastmcp import FastMCP

from catalog import describe_dataset as describe_impl  # noqa: E402
from catalog import list_datasets as list_impl  # noqa: E402
from catalog import resolve_parquet_path  # noqa: E402

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
TOKEN_RE = re.compile(r"[a-z_][a-z0-9_]*")


class DuckdbClientError(RuntimeError):
    pass


def _guard_max_rows(max_rows: int) -> int:
    if max_rows <= 0:
        raise DuckdbClientError("max_rows deve essere maggiore di 0")
    if max_rows > MAX_ROWS_HARD_CAP:
        raise DuckdbClientError(
            f"max_rows oltre il limite hard cap di {MAX_ROWS_HARD_CAP}"
        )
    return max_rows


def _validate_select_sql(sql: str) -> str:
    text = (sql or "").strip()
    if not text:
        raise DuckdbClientError("sql vuoto")

    lowered = text.lower()
    if ";" in text:
        raise DuckdbClientError("Query multiple o statement terminati da ';' non consentiti")
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise DuckdbClientError("Sono consentite solo query SELECT o WITH")

    scrubbed = re.sub(r"--.*?$", " ", text, flags=re.MULTILINE)
    scrubbed = re.sub(r"/\*.*?\*/", " ", scrubbed, flags=re.DOTALL)
    scrubbed = re.sub(r"'(?:''|[^'])*'", " ", scrubbed)
    scrubbed = re.sub(r'"(?:""|[^"])*"', " ", scrubbed)
    tokens = {token.lower() for token in TOKEN_RE.findall(scrubbed)}

    for keyword in BLOCKED_KEYWORDS:
        if keyword in tokens:
            raise DuckdbClientError(f"Keyword non consentita nella query: {keyword}")
    return text


def guard(fn, handled_exceptions: tuple[type[BaseException], ...] = (Exception,)) -> dict[str, Any]:
    try:
        return fn()
    except handled_exceptions as exc:
        return {"error": str(exc)}


def mcp_telemetry(_server: str):
    def decorator(fn):
        return fn

    return decorator


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
            "Usa 'FROM clean_input' invece di read_parquet()."
        )
    if "read_csv(" in scrubbed_lower:
        raise DuckdbClientError(
            "Accesso diretto a read_csv() non consentito. Usa 'FROM clean_input'."
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
            f"Usa describe_dataset() per lo schema."
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
            f"Usa describe_dataset() per lo schema."
        )


mcp = FastMCP(
    name="clean-query",
    instructions=(
        "MCP server per interrogare i dataset clean del DataCivicLab tramite DuckDB. "
        "Espone catalogo semantico (dataset, colonne, metriche) e esecuzione query read-only. "
        "Il client AI (Claude/Qwen/etc.) genera il SQL a partire dallo schema."
    ),
)


@mcp.tool(
    description="Lista dei dataset clean disponibili per query.", structured_output=True
)
@mcp_telemetry("clean-query")
def list_datasets() -> list[dict[str, Any]]:
    return list_impl()


@mcp.tool(
    description="Descrive lo schema di un dataset: colonne, tipi, ruolo (dimension/metric), periodo.",
    structured_output=True,
)
@mcp_telemetry("clean-query")
def describe_dataset(slug: str) -> dict[str, Any]:
    return describe_impl(slug)


@mcp.tool(
    description=(
        "Esegue una query SQL read-only su un dataset clean tramite DuckDB. "
        "Solo SELECT/WITH. Il SQL deve riferire SOLO 'FROM clean_input' o CTE locali. "
        "I path ai parquet sono risolti automaticamente dal catalogo. "
        "Hard cap: max 500 righe, timeout 60s. "
        "Per dataset multi-anno, usare year per filtrare (opzionale)."
    ),
    structured_output=True,
)
@mcp_telemetry("clean-query")
def run_query(
    sql: str, dataset: str, max_rows: int = 100, year: int | None = None
) -> dict[str, Any]:
    try:
        parquet_paths = resolve_parquet_path(dataset, year=year)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc)}

    # Scope enforcement: only clean_input and local CTEs in FROM/JOIN clauses.
    try:
        _validate_scope(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    # Hygiene checks: no DDL/DML, blocked keywords.
    try:
        _validate_select_sql(sql)
    except DuckdbClientError as exc:
        return {"error": str(exc)}

    # Build the SQL wrapping user query.
    # For multi-file datasets, DuckDB reads a list of URLs directly.
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

        import duckdb
        import concurrent.futures

        conn = duckdb.connect(database=":memory:")
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
            conn.close()
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

    return guard(_exec, handled_exceptions=(DuckdbClientError, Exception))


@mcp.tool(
    description="Restituisce statistiche sulla cache GCS del catalogo (utile per debug).",
    structured_output=True,
)
@mcp_telemetry("clean-query")
def cache_stats() -> dict[str, Any]:
    from catalog import gcs_cache_stats

    return gcs_cache_stats()


if __name__ == "__main__":
    mcp.run()
