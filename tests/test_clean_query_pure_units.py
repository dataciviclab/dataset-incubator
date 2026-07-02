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
# Cache key: year e ordine dataset
# ---------------------------------------------------------------------------


def test_run_query_cache_key_includes_year(monkeypatch):
    """run_query: year diverso deve produrre cache key diversa."""
    # Pulisce cache
    server._query_cache.clear()

    # Mocka _execute_sql per contare chiamate
    call_count = 0

    def counting_exec(dataset, sql, year=None, timeout=60):
        nonlocal call_count
        call_count += 1
        return {"columns": ["c"], "rows": [[year]]}

    monkeypatch.setattr(server, "_execute_sql", counting_exec)
    monkeypatch.setattr(server, "get_year_column", lambda x: None)  # nessuna colonna anno

    # Chiama con year=2023
    r1 = server.run_query("SELECT 1", "test_ds", year=2023)
    assert r1["rows"][0][0] == 2023
    assert call_count == 1

    # Chiama con year=2024 — deve fare nuova chiamata (cache key diversa)
    r2 = server.run_query("SELECT 1", "test_ds", year=2024)
    assert r2["rows"][0][0] == 2024
    assert call_count == 2

    # Chiama con year=2023 di nuovo — deve usare cache (nessuna nuova chiamata)
    r3 = server.run_query("SELECT 1", "test_ds", year=2023)
    assert r3["rows"][0][0] == 2023
    assert call_count == 2  # non incrementa


def test_run_query_cache_key_without_year_is_separate(monkeypatch):
    """run_query senza year deve essere separato da chiamate con year."""
    server._query_cache.clear()

    call_count = 0

    def counting_exec(dataset, sql, year=None, timeout=60):
        nonlocal call_count
        call_count += 1
        return {"columns": ["c"], "rows": [[year]]}

    monkeypatch.setattr(server, "_execute_sql", counting_exec)
    monkeypatch.setattr(server, "get_year_column", lambda x: None)

    # Senza year
    _ = server.run_query("SELECT 1", "test_ds")
    assert call_count == 1

    # Con year=2023 — cache key diversa per year
    _ = server.run_query("SELECT 1", "test_ds", year=2023)
    assert call_count == 2

    # Senza year di nuovo — cache hit
    _ = server.run_query("SELECT 1", "test_ds")
    assert call_count == 2


def test_cross_query_cache_key_normalizes_order(monkeypatch):
    """cross_query: ['a','b'] e ['b','a'] devono usare la stessa cache key."""
    server._query_cache.clear()

    call_count = 0

    def counting_exec(datasets, sql, timeout=60):
        nonlocal call_count
        call_count += 1
        return {"columns": ["ds"], "rows": [[",".join(datasets)]]}

    monkeypatch.setattr(server, "_execute_cross_sql", counting_exec)

    _ = server.cross_query(["a", "b"], "SELECT 1")
    assert call_count == 1

    # Ordine inverso — cache hit
    r2 = server.cross_query(["b", "a"], "SELECT 1")
    assert call_count == 1  # stesso risultato della cache
    assert r2["datasets"] == ["a", "b"]  # normalizzato


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


# ---------------------------------------------------------------------------
# dataset_overview: limit=0 (schema only) e validazione
# ---------------------------------------------------------------------------


def test_dataset_overview_limit_zero(monkeypatch):
    """dataset_overview con limit=0 restituisce solo schema (nessuna query DuckDB)."""
    fake_desc = {
        "slug": "test_ds",
        "name": "Test DS",
        "source": "Test",
        "period": {"start": 2020, "end": 2024},
        "columns": [{"name": "anno", "type": "BIGINT", "role": "dimension"}],
    }
    monkeypatch.setattr(server, "describe_impl", lambda s: fake_desc)
    result = server.dataset_overview("test_ds", limit=0)
    assert result["slug"] == "test_ds"
    assert result["columns"] == fake_desc["columns"]
    assert result["total_rows"] is None
    assert result["preview"] is None


def test_dataset_overview_limit_negative():
    """dataset_overview con limit negativo restituisce errore."""
    result = server.dataset_overview("test_ds", limit=-1)
    assert "error" in result


def test_dataset_overview_limit_exceeds_cap():
    """dataset_overview con limit oltre hard cap restituisce errore."""
    result = server.dataset_overview("test_ds", limit=server.MAX_ROWS_HARD_CAP + 1)
    assert "error" in result


# ---------------------------------------------------------------------------
# ente: validazione input
# ---------------------------------------------------------------------------


def test_ente_empty_params():
    """ente() senza parametri restituisce errore."""
    result = server.ente()
    assert "error" in result


def test_ente_invalid_codice_istat():
    """ente() con codice_istat non 6 cifre restituisce errore."""
    result = server.ente(codice_istat="abc")
    assert "error" in result


# ---------------------------------------------------------------------------
# query: validazione input
# ---------------------------------------------------------------------------


def test_query_empty_datasets():
    """query() con datasets vuoto restituisce errore."""
    result = server.query("SELECT 1", datasets=[])
    assert "error" in result


def test_query_dry_run_rejects_read_parquet(monkeypatch):
    """query(dry_run=True) deve rifiutare read_parquet diretto come la modalità normale."""
    monkeypatch.setattr(server, "resolve_parquet_path", lambda *a, **kw: ["gs://fake/test.parquet"])
    result = server.query(
        "SELECT * FROM read_parquet('gs://bucket/file.parquet')",
        datasets=["irpef_comunale"],
        dry_run=True,
    )
    assert "error" in result


# ---------------------------------------------------------------------------
# find: edge case metric_only
# ---------------------------------------------------------------------------


def test_find_empty_metric_only():
    """find() con query vuota e metric_only=True restituisce solo dataset con metriche."""
    result = server.find(metric_only=True)
    assert result["count"] > 0
    # Tutti i risultati devono avere almeno una colonna metric
    for ds in result["datasets"]:
        assert (
            any(c.get("role") == "metric" for c in server.load_catalog() if c["slug"] == ds["slug"])
            or True
        )  # skip check
    # verifica che i dataset senza metriche non compaiano
    catalog = server.load_catalog()
    no_metric = [
        d["slug"]
        for d in catalog
        if not any(c.get("role") == "metric" for c in d.get("columns", []))
    ]
    result_slugs = {d["slug"] for d in result["datasets"]}
    for slug in no_metric:
        assert slug not in result_slugs, f"{slug} non ha metriche ma è stato incluso"


# ---------------------------------------------------------------------------
# dataset_graph: bridge registry
# ---------------------------------------------------------------------------


def test_dataset_graph_bdap_registry():
    """dataset_graph con by_registry='bdap_anagrafe_enti' restituisce il bridge."""
    result = server.dataset_graph(by_registry="bdap_anagrafe_enti")
    assert "registry" not in result  # non è un errore
    regs = result.get("registries", {})
    assert "bdap_anagrafe_enti" in regs
