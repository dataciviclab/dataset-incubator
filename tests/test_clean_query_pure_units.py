"""Test unitari puri per server.py — zero I/O, zero mock.

Funzioni di validazione e helper senza dipendenze esterne.
"""

from __future__ import annotations

import pytest

from tools.clean_query_mcp import server

pytestmark = pytest.mark.pure_unit


class TestGuardMaxRows:
    def test_returns_valid_value(self):
        assert server._guard_max_rows(100) == 100

    def test_zero_raises(self):
        with pytest.raises(server.DuckdbClientError):
            server._guard_max_rows(0)

    def test_above_hard_cap_raises(self):
        with pytest.raises(server.DuckdbClientError):
            server._guard_max_rows(server.MAX_ROWS_HARD_CAP + 1)


class TestValidateSelectSql:
    def test_allows_valid_select(self):
        assert (
            server._validate_select_sql("SELECT * FROM clean_input") == "SELECT * FROM clean_input"
        )

    def test_allows_with(self):
        assert server._validate_select_sql("WITH t AS (SELECT 1) SELECT * FROM t")

    def test_rejects_none(self):
        with pytest.raises(server.DuckdbClientError, match="sql vuoto"):
            server._validate_select_sql(None)  # type: ignore[arg-type]

    def test_rejects_empty(self):
        with pytest.raises(server.DuckdbClientError, match="sql vuoto"):
            server._validate_select_sql("")

    def test_rejects_whitespace(self):
        with pytest.raises(server.DuckdbClientError, match="sql vuoto"):
            server._validate_select_sql("   ")

    def test_rejects_semicolon(self):
        with pytest.raises(server.DuckdbClientError, match="';'"):
            server._validate_select_sql("SELECT * FROM clean_input;")

    def test_rejects_non_select(self):
        with pytest.raises(server.DuckdbClientError, match="SELECT o WITH"):
            server._validate_select_sql("DELETE FROM clean_input")

    def test_rejects_blocked_keyword(self):
        with pytest.raises(server.DuckdbClientError, match="Keyword non consentita"):
            server._validate_select_sql("select * from clean_input install something")

    def test_rejects_blocked_keyword_uppercase(self):
        """Il regex TOKEN_RE ora usa re.IGNORECASE — INSTALL deve essere bloccato."""
        with pytest.raises(server.DuckdbClientError, match="Keyword non consentita"):
            server._validate_select_sql("select * from clean_input INSTALL something")

    def test_rejects_blocked_keyword_mixed_case(self):
        """Anche InStAlL misto deve essere bloccato."""
        with pytest.raises(server.DuckdbClientError, match="Keyword non consentita"):
            server._validate_select_sql("select * from clean_input InStAlL something")

    def test_allows_keyword_in_string_literal(self):
        """Keyword dentro stringa letterale non deve falsamente bloccare."""
        server._validate_select_sql("select * from clean_input where note = 'INSTALL OK'")


class TestValidateParquetPaths:
    def test_accepts_safe_path(self):
        server._validate_parquet_paths(["gs://bucket/dataset/2024/file.parquet"])

    def test_rejects_unsafe_char(self):
        with pytest.raises(server.DuckdbClientError, match="caratteri non sicuri"):
            server._validate_parquet_paths(["gs://bucket/file with spaces.parquet"])

    def test_rejects_backslash(self):
        with pytest.raises(server.DuckdbClientError):
            server._validate_parquet_paths(["gs://bucket\\file.parquet"])


class TestValidateScope:
    def test_allows_clean_input_from(self):
        server._validate_scope("SELECT COUNT(*) FROM clean_input")

    def test_allows_join_clean_input(self):
        server._validate_scope("SELECT * FROM clean_input JOIN clean_input AS ci USING (id)")

    def test_blocks_read_parquet(self):
        with pytest.raises(server.DuckdbClientError, match="read_parquet"):
            server._validate_scope("SELECT * FROM read_parquet('gs://bucket/file.parquet')")

    def test_blocks_read_csv(self):
        with pytest.raises(server.DuckdbClientError, match="read_csv"):
            server._validate_scope("SELECT * FROM read_csv('file.csv')")

    def test_blocks_unknown_from(self):
        with pytest.raises(server.DuckdbClientError, match="non consentito in FROM"):
            server._validate_scope("SELECT * FROM other_table")

    def test_blocks_unknown_join(self):
        with pytest.raises(server.DuckdbClientError, match="non consentito in JOIN"):
            server._validate_scope("SELECT * FROM clean_input JOIN other_table USING (id)")


class TestInjectYearFilterEdgeCases:
    """Rami non coperti dai test esistenti di _inject_year_filter."""

    def test_no_from_returns_unchanged(self):
        """Linea 278: nessun FROM clean_input -> sql invariato."""
        sql = "SELECT 1"
        result = server._inject_year_filter(sql, "anno", 2024)
        assert result == sql

    def test_where_already_present(self):
        """Linea 283-284: WHERE gia' presente -> non duplica."""
        sql = "SELECT * FROM clean_input WHERE altro_col > 0"
        result = server._inject_year_filter(sql, "anno", 2024)
        assert result.count("WHERE") == 1

    def test_with_before_keyword_preserves_space(self):
        """Linea 293-294: prima della keyword c'e' spazio extra."""
        sql = "SELECT * FROM clean_input  ORDER BY 1"
        result = server._inject_year_filter(sql, "anno", 2024)
        assert "WHERE anno = 2024" in result
        assert "ORDER BY" in result

    def test_tail_not_empty_no_keyword(self):
        """Linea 299-300: tail presente ma nessuna keyword riconosciuta (es. SAMPLE)."""
        sql = "SELECT * FROM clean_input SAMPLE 10"
        result = server._inject_year_filter(sql, "anno", 2024)
        assert "WHERE anno = 2024" in result
        assert "SAMPLE" in result


# ---------------------------------------------------------------------------
# Tool delegation: mocka impl catalog, verifica forwarding parametri
# ---------------------------------------------------------------------------

_SEARCH_FIXTURE = [
    {"slug": "test_a", "name": "Test A", "source": "source_1"},
    {"slug": "test_b", "name": "Test B", "source": "source_2"},
]

_DESCRIBE_FIXTURE = {
    "slug": "test_a",
    "columns": [
        {"name": "anno", "type": "BIGINT", "role": "dimension"},
        {"name": "valore", "type": "DOUBLE", "role": "metric"},
    ],
    "period": {"start_year": 2020, "end_year": 2024},
}


def test_list_datasets(monkeypatch):
    monkeypatch.setattr(server, "list_impl", lambda: _SEARCH_FIXTURE)
    result = server.list_datasets()
    assert result == _SEARCH_FIXTURE


def test_describe_dataset_valid(monkeypatch):
    monkeypatch.setattr(server, "describe_impl", lambda slug: _DESCRIBE_FIXTURE)
    result = server.describe_dataset("test_a")
    assert result["slug"] == "test_a"
    assert len(result["columns"]) == 2


def test_describe_dataset_not_found(monkeypatch):
    monkeypatch.setattr(server, "describe_impl", lambda slug: {"error": "not found"})
    result = server.describe_dataset("nonexistent")
    assert "error" in result


def test_search_datasets_valid(monkeypatch):
    monkeypatch.setattr(server, "search_impl", lambda q: _SEARCH_FIXTURE)
    result = server.search_datasets("test")
    assert result["datasets"] == _SEARCH_FIXTURE
    assert result["query"] == "test"


def test_search_datasets_empty_query():
    result = server.search_datasets("")
    assert "error" in result


def test_cache_stats(monkeypatch):
    from tools.clean_query_mcp import catalog

    monkeypatch.setattr(
        catalog, "gcs_cache_stats", lambda: {"parquet_files": 10, "cached_bytes": 1000}
    )
    result = server.cache_stats()
    assert result["parquet_files"] == 10


# ---------------------------------------------------------------------------
# dataset_overview: test mockati, nessun DuckDB reale
# ---------------------------------------------------------------------------

_OVERVIEW_SLUG = "test_overview"
_OVERVIEW_COLS = [
    {"name": "anno", "type": "BIGINT", "role": "dimension"},
    {"name": "regione", "type": "VARCHAR", "role": "dimension"},
    {"name": "valore", "type": "DOUBLE", "role": "metric"},
]
_OVERVIEW_DESC = {
    "slug": _OVERVIEW_SLUG,
    "name": "Test Overview",
    "description": "Un dataset di test",
    "source": "Test Source",
    "period": {"start_year": 2020, "end_year": 2024},
    "columns": _OVERVIEW_COLS,
}


class TestDatasetOverview:
    def test_limit_invalid(self, monkeypatch):
        """Limite fuori range -> errore."""
        result = server.dataset_overview(_OVERVIEW_SLUG, limit=0)
        assert "error" in result

    def test_limit_exceeds_hard_cap(self, monkeypatch):
        result = server.dataset_overview(_OVERVIEW_SLUG, limit=server.MAX_ROWS_HARD_CAP + 1)
        assert "error" in result

    def test_schema_error_propagated(self, monkeypatch):
        monkeypatch.setattr(server, "describe_impl", lambda s: {"error": "not found"})
        result = server.dataset_overview("inesistente")
        assert "error" in result

    def test_execute_sql_error_propagated(self, monkeypatch):
        """Se _execute_sql fallisce, l'errore è nel risultato."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)

        def fake_execute(*args, **kwargs):
            return {"error": "simulated duckdb error"}

        monkeypatch.setattr(server, "_execute_sql", fake_execute)
        result = server.dataset_overview(_OVERVIEW_SLUG)
        assert "error" in result
        assert "simulated" in result["error"]

    def test_returns_schema_fields(self, monkeypatch):
        """I campi dello schema sono presenti nell'output."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(
            server,
            "_execute_sql",
            lambda *a, **kw: {
                "columns": ["anno", "regione", "valore", "total_rows"],
                "rows": [[2020, "Lombardia", 100.0, 5]],
            },
        )
        result = server.dataset_overview(_OVERVIEW_SLUG)
        assert result["slug"] == _OVERVIEW_SLUG
        assert result["name"] == "Test Overview"
        assert result["total_rows"] == 5
        assert result["preview"]["row_count"] == 1

    def test_preview_columns_exclude_total_rows(self, monkeypatch):
        """La colonna total_rows non deve apparire nelle preview columns."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(
            server,
            "_execute_sql",
            lambda *a, **kw: {
                "columns": ["anno", "regione", "valore", "total_rows"],
                "rows": [[2020, "Lombardia", 100.0, 5]],
            },
        )
        result = server.dataset_overview(_OVERVIEW_SLUG)
        assert "total_rows" not in result["preview"]["columns"]
        assert result["preview"]["columns"] == ["anno", "regione", "valore"]

    def test_empty_dataset(self, monkeypatch):
        """Dataset vuoto -> total_rows = 0, preview vuoto."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(
            server,
            "_execute_sql",
            lambda *a, **kw: {
                "columns": ["anno", "regione", "valore", "total_rows"],
                "rows": [],
            },
        )
        result = server.dataset_overview(_OVERVIEW_SLUG)
        assert result["total_rows"] == 0
        assert result["preview"]["row_count"] == 0
