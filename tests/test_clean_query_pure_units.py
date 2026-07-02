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
        catalog,
        "gcs_cache_stats",
        lambda: {"total_entries": 2, "valid_entries": 2, "ttl_sec": 300, "entries": []},
    )
    result = server.cache_stats()
    assert "gcs_path_resolution" in result
    assert "query_results" in result
    assert result["gcs_path_resolution"]["total_entries"] == 2


def test_column_search(monkeypatch):
    """column_search cerca in nome dataset, descrizione e colonne."""
    fake_catalog = [
        {
            "slug": "ds_redditi",
            "name": "Redditi Comunali",
            "description": "Dati reddito per comune",
            "source": "MEF",
            "period": {"start": 2020, "end": 2024},
            "columns": [
                {"name": "anno", "type": "BIGINT", "role": "dimension"},
                {
                    "name": "regione",
                    "type": "VARCHAR",
                    "role": "dimension",
                    "description": "Regione",
                },
                {
                    "name": "reddito_totale",
                    "type": "DOUBLE",
                    "role": "metric",
                    "description": "Reddito totale",
                },
            ],
        },
        {
            "slug": "ds_popolazione",
            "name": "Popolazione",
            "description": "Popolazione italiana",
            "source": "ISTAT",
            "period": {"start": 2022, "end": 2024},
            "columns": [
                {"name": "anno", "type": "BIGINT", "role": "dimension"},
                {"name": "popolazione", "type": "BIGINT", "role": "metric"},
            ],
        },
    ]
    monkeypatch.setattr(server, "load_catalog", lambda: fake_catalog)

    # Match per nome colonna
    res = server.column_search("reddito")
    assert res["count"] == 1
    assert res["datasets"][0]["slug"] == "ds_redditi"
    assert len(res["datasets"][0]["matched_columns"]) == 1

    # Match per meta dataset
    res = server.column_search("popolazione")
    assert res["count"] == 1
    assert res["datasets"][0]["meta_match"] is True

    # Nessun match
    res = server.column_search("xyz_notfound")
    assert res["count"] == 0


def test_find_metric_datasets(monkeypatch):
    """find_metric_datasets cerca dataset con colonne role=metric."""
    fake_catalog = [
        {
            "slug": "ds_con_metriche",
            "name": "Con Metriche",
            "source": "Test",
            "period": {"start": 2020, "end": 2024},
            "columns": [
                {"name": "valore", "type": "DOUBLE", "role": "metric", "description": "Valore"},
            ],
        },
        {
            "slug": "ds_senza_metriche",
            "name": "Senza Metriche",
            "source": "Test",
            "period": {"start": 2020, "end": 2024},
            "columns": [
                {"name": "nome", "type": "VARCHAR", "role": "dimension"},
            ],
        },
    ]
    monkeypatch.setattr(server, "load_catalog", lambda: fake_catalog)

    res = server.find_metric_datasets()
    assert res["count"] == 1
    assert res["datasets"][0]["slug"] == "ds_con_metriche"
    assert len(res["datasets"][0]["metric_columns"]) == 1

    # Filtro per nome metrica
    res = server.find_metric_datasets(metric_name="valore")
    assert res["count"] == 1

    # Filtro per nome metrica inesistente
    res = server.find_metric_datasets(metric_name="fake_metric")
    assert res["count"] == 0

    # Filtro per query
    res = server.find_metric_datasets(query="metriche")
    assert res["count"] == 1

    # Query senza match
    res = server.find_metric_datasets(query="xyz")
    assert res["count"] == 0


# ---------------------------------------------------------------------------
# dataset_overview: test mockati, nessun DuckDB reale
# ---------------------------------------------------------------------------

_OVERVIEW_COLS = [
    {"name": "anno", "type": "BIGINT", "role": "dimension"},
    {"name": "regione", "type": "VARCHAR", "role": "dimension"},
    {"name": "valore", "type": "DOUBLE", "role": "metric"},
]
_OVERVIEW_DESC = {
    "slug": "test_overview",
    "name": "Test Overview",
    "description": "Un dataset di test",
    "source": "Test Source",
    "period": {"start_year": 2020, "end_year": 2024},
    "columns": _OVERVIEW_COLS,
}

_COUNT_OK = [{"columns": ["total"], "rows": [[5]]}]
_PREVIEW_OK = [{"columns": ["anno", "regione", "valore"], "rows": [[2020, "Lombardia", 100.0]]}]
_BATCH_OK = _COUNT_OK + _PREVIEW_OK
_BATCH_ERR = [{"error": "simulated duckdb error"}, {"error": "simulated duckdb error"}]
_BATCH_EMPTY = [
    {"columns": ["total"], "rows": [[0]]},
    {"columns": ["anno", "regione", "valore"], "rows": []},
]


class TestDatasetOverview:
    def setup_method(self):
        """Pulisce la cache query tra un test e l'altro."""
        server._query_cache.clear()

    def test_limit_invalid(self):
        result = server.dataset_overview("test_overview", limit=0)
        assert "error" in result

    def test_limit_exceeds_hard_cap(self):
        result = server.dataset_overview("test_overview", limit=server.MAX_ROWS_HARD_CAP + 1)
        assert "error" in result

    def test_schema_error_propagated(self, monkeypatch):
        monkeypatch.setattr(server, "describe_impl", lambda s: {"error": "not found"})
        result = server.dataset_overview("inesistente")
        assert "error" in result

    def test_batch_error_propagated(self, monkeypatch):
        """Se _execute_sql_batch fallisce, l'errore è nel risultato."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_ERR)
        # Usa slug diverso per evitare cache
        result = server.dataset_overview("overview_batch_err")
        assert "error" in result
        assert "simulated" in result["error"]

    def test_returns_schema_fields(self, monkeypatch):
        """I campi dello schema sono presenti nell'output."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_OK)
        result = server.dataset_overview("overview_fields")
        assert result["slug"] == "overview_fields"
        assert result["name"] == "Test Overview"
        assert result["total_rows"] == 5
        assert result["preview"]["row_count"] == 1
        assert result["_cached"] is False

    def test_cache_hit(self, monkeypatch):
        """Seconda chiamata con stesso slug+limit deve tornare cached."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_OK)
        # Prima chiamata — popola cache
        r1 = server.dataset_overview("overview_cache_test")
        assert r1["total_rows"] == 5
        assert r1["_cached"] is False

        # Seconda chiamata — deve venire da cache (describe_impl non mockato fallirebbe)
        monkeypatch.setattr(server, "describe_impl", lambda s: {"error": "should not be called"})
        r2 = server.dataset_overview("overview_cache_test")
        assert r2["total_rows"] == 5

    def test_preview_columns_structure(self, monkeypatch):
        """Le preview columns non devono contenere campi aggiuntivi."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_OK)
        result = server.dataset_overview("overview_preview_cols")
        assert result["preview"]["columns"] == ["anno", "regione", "valore"]

    def test_preview_rows_type(self, monkeypatch):
        """Le righe di preview sono liste (non tuple)."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_OK)
        result = server.dataset_overview("overview_rows_type")
        row = result["preview"]["rows"][0]
        assert isinstance(row, list)
        assert row == [2020, "Lombardia", 100.0]

    def test_empty_dataset(self, monkeypatch):
        """Dataset vuoto -> total_rows = 0, preview vuoto."""
        monkeypatch.setattr(server, "describe_impl", lambda s: _OVERVIEW_DESC)
        monkeypatch.setattr(server, "_execute_sql_batch", lambda *a, **kw: _BATCH_EMPTY)
        result = server.dataset_overview("overview_empty")
        assert result["total_rows"] == 0
        assert result["preview"]["row_count"] == 0


# ---------------------------------------------------------------------------
# _validate_cross_scope: validazione query su più dataset
# ---------------------------------------------------------------------------


class TestValidateCrossScope:
    def test_allows_allowed_tables_from(self):
        """FROM con tabella nella allowed_tables è permesso."""
        server._validate_cross_scope(
            "SELECT * FROM irpef_comunale WHERE anno = 2024",
            {"irpef_comunale"},
        )

    def test_allows_allowed_tables_join(self):
        """JOIN con tabella nella allowed_tables è permesso."""
        server._validate_cross_scope(
            "SELECT * FROM irpef_comunale i JOIN popolazione p ON i.id = p.id",
            {"irpef_comunale", "popolazione"},
        )

    def test_allows_cte_plus_tables(self):
        """CTE locali + allowed_tables sono tutte permesse."""
        server._validate_cross_scope(
            "WITH filtered AS (SELECT * FROM irpef_comunale) "
            "SELECT * FROM filtered JOIN popolazione ON filtered.id = popolazione.id",
            {"irpef_comunale", "popolazione"},
        )

    def test_blocks_unknown_from(self):
        """FROM con tabella non in allowed_tables è bloccato."""
        with pytest.raises(server.DuckdbClientError, match="non consentito in FROM"):
            server._validate_cross_scope(
                "SELECT * FROM other_table",
                {"irpef_comunale"},
            )

    def test_blocks_unknown_join(self):
        """JOIN con tabella non in allowed_tables è bloccato."""
        with pytest.raises(server.DuckdbClientError, match="non consentito in JOIN"):
            server._validate_cross_scope(
                "SELECT * FROM irpef_comunale JOIN other_table ON irpef_comunale.id = other_table.id",
                {"irpef_comunale"},
            )

    def test_blocks_read_parquet(self):
        """read_parquet è bloccato anche in cross scope."""
        with pytest.raises(server.DuckdbClientError, match="read_parquet"):
            server._validate_cross_scope(
                "SELECT * FROM read_parquet('gs://bucket/file.parquet')",
                {"irpef_comunale"},
            )

    def test_blocks_read_csv(self):
        """read_csv è bloccato anche in cross scope."""
        with pytest.raises(server.DuckdbClientError, match="read_csv"):
            server._validate_cross_scope(
                "SELECT * FROM read_csv('file.csv')",
                {"irpef_comunale"},
            )

    def test_empty_sql_blocks(self):
        """SQL vuoto non passa."""
        with pytest.raises(server.DuckdbClientError):
            server._validate_select_sql("")

    def test_blocks_from_string_literal(self):
        """FROM 'url.parquet' bypassa la whitelist — deve essere bloccato."""
        with pytest.raises(server.DuckdbClientError, match="non consentito"):
            server._validate_cross_scope(
                "SELECT * FROM 'https://storage.googleapis.com/bucket/aifa_spesa_consumo/file.parquet' LIMIT 1",
                {"irpef_comunale", "popolazione_istat_comunale_2019_2025"},
            )

    def test_blocks_join_string_literal(self):
        """JOIN 'url.parquet' deve essere bloccato come FROM."""
        with pytest.raises(server.DuckdbClientError, match="non consentito"):
            server._validate_cross_scope(
                "SELECT * FROM irpef_comunale JOIN 'gs://bucket/other.parquet' AS o ON 1=1",
                {"irpef_comunale"},
            )

    def test_allows_safe_string_in_where(self):
        """Stringhe letterali in WHERE non devono scatenare falsi positivi."""
        server._validate_cross_scope(
            "SELECT * FROM irpef_comunale WHERE denominazione_comune = 'Milano'",
            {"irpef_comunale"},
        )

    def test_allows_safe_string_in_values(self):
        """Stringhe letterali in VALUES o IN non devono essere bloccate."""
        server._validate_cross_scope(
            "SELECT * FROM irpef_comunale WHERE comune IN ('Milano', 'Roma')",
            {"irpef_comunale"},
        )


# ---------------------------------------------------------------------------
# _load_relationship_map: carica il JSON committed in registry/
# ---------------------------------------------------------------------------


def test_relationship_map_loads():
    """relationship_map.json deve esistere ed essere un dict valido."""
    result = server._load_relationship_map()
    assert "error" not in result, f"Errore caricamento relationship_map: {result.get('error')}"
    assert "registries" in result
    assert "comuni_master" in result["registries"]
    assert "description" in result
    assert "unconnected_datasets" in result


def test_dataset_graph_full_map():
    """dataset_graph() senza filtri restituisce la mappa completa."""
    result = server.dataset_graph()
    assert "summary" in result
    assert result["summary"]["registries"] >= 1
    assert result["summary"]["datasets"] >= 10
    assert "tip" in result


def test_dataset_graph_by_key():
    """dataset_graph(by_key='codice_istat') filtra per chiave."""
    result = server.dataset_graph(by_key="codice_istat")
    reg = result.get("registries", {}).get("comuni_master", {}).get("keys", {})
    assert "codice_istat" in reg
    # Non devono apparire chiavi che non contengono 'codice_istat'
    for key_name in reg:
        assert "codice_istat" in key_name.lower()


def test_dataset_graph_by_dataset():
    """dataset_graph(by_dataset='irpef') trova il dataset."""
    result = server.dataset_graph(by_dataset="irpef")
    # Deve comparire in almeno una chiave
    found = False
    for reg in result.get("registries", {}).values():
        for key in reg.get("keys", {}).values():
            for ds in key.get("datasets", []):
                if "irpef" in ds["slug"].lower():
                    found = True
    assert found, "irpef_comunale non trovato in nessuna chiave"


def test_dataset_graph_unknown_key():
    """dataset_graph(by_key='inesistente') restituisce mappa vuota."""
    result = server.dataset_graph(by_key="xyz_notfound_123")
    assert len(result.get("registries", {})) == 0
    assert result.get("summary", {}).get("datasets", -1) == 0


def test_dataset_graph_unknown_registry():
    """dataset_graph(by_registry='inesistente') restituisce errore."""
    result = server.dataset_graph(by_registry="fake_registry")
    assert "error" in result


# ---------------------------------------------------------------------------
# cross_query: validazione input
# ---------------------------------------------------------------------------


def test_cross_query_requires_at_least_two_datasets():
    """cross_query con <2 dataset deve fallire subito."""
    result = server.cross_query(datasets=["irpef_comunale"], sql="SELECT 1")
    assert "error" in result
    assert "almeno 2" in result["error"].lower()


def test_cross_query_invalid_max_rows():
    """cross_query con max_rows fuori range deve sollevare DuckdbClientError."""
    with pytest.raises(server.DuckdbClientError):
        server.cross_query(
            datasets=["irpef_comunale", "popolazione_istat_comunale_2019_2025"],
            sql="SELECT 1",
            max_rows=0,
        )


# ---------------------------------------------------------------------------
# Entry point, cache GCS
# ---------------------------------------------------------------------------


def test_main_exists():
    """main() è callable (non la eseguiamo, bloccherebbe il server)."""
    assert callable(server.main)


def test_gcs_cache_clear(monkeypatch):
    """gcs_cache_clear pulisce la cache GCS."""
    from tools.clean_query_mcp import catalog as cat_mod

    # Popola cache con un entry finto
    cat_mod._gcs_res_cache[("test", 2024)] = (1000.0, ["gs://fake/test.parquet"])
    cat_mod.gcs_cache_clear()
    stats = cat_mod.gcs_cache_stats()
    assert stats["total_entries"] == 0
    assert stats["valid_entries"] == 0
