"""Test unitari puri per catalog.py — zero I/O esterno.

Contratto:
  - _gcs_auth_mode: parsing env CLEAN_QUERY_GCS_AUTH
  - _glob_to_regex:  conversione glob → regex
  - get_year_column: rilevamento colonna anno da schema
  - list_datasets / describe_dataset / search_datasets: interrogazione catalogo
  - gcs_cache_stats / gcs_cache_clear: gestione cache GCS
"""

from __future__ import annotations


import pytest

from tools.clean_query_mcp import catalog

pytestmark = pytest.mark.pure_unit

# ---------------------------------------------------------------------------
# Campione catalogo per test
# ---------------------------------------------------------------------------

_SAMPLE_CATALOG = [
    {
        "slug": "test_single",
        "name": "Test Single",
        "description": "Dataset singolo per test",
        "source": "test_source",
        "period": {"start": 2020, "end": 2024},
        "location": {"type": "local", "path": "data/test_single.parquet"},
        "columns": [
            {"name": "anno", "type": "INTEGER", "role": "dimension"},
            {"name": "valore", "type": "DOUBLE", "role": "metric"},
        ],
    },
    {
        "slug": "test_multi",
        "name": "Test Multi Year",
        "description": "Dataset multi-anno per test",
        "source": "test_source",
        "period": {"start": 2019, "end": 2023},
        "location": {
            "type": "gcs",
            "path": "gs://bucket/test_multi/*/test_multi_*_clean.parquet",
            "multi_file": True,
        },
        "columns": [
            {"name": "anno_di_imposta", "type": "BIGINT", "role": "dimension"},
            {"name": "regione", "type": "VARCHAR", "role": "dimension"},
            {"name": "valore", "type": "DOUBLE", "role": "metric"},
        ],
    },
    {
        "slug": "test_no_anno",
        "name": "Test No Anno",
        "description": "Dataset senza colonna anno",
        "source": "other_source",
        "period": {"start": 2022, "end": 2022},
        "location": {"type": "local", "path": "data/test_no_anno.parquet"},
        "columns": [
            {"name": "categoria", "type": "VARCHAR", "role": "dimension"},
            {"name": "valore", "type": "DOUBLE", "role": "metric"},
        ],
    },
    {
        "slug": "test_string_anno",
        "name": "Test String Anno",
        "description": "Dataset con colonna anno VARCHAR",
        "source": "other_source",
        "period": {"start": 2020, "end": 2023},
        "location": {"type": "local", "path": "data/test_string_anno.parquet"},
        "columns": [
            {"name": "anno", "type": "VARCHAR", "role": "dimension"},
            {"name": "valore", "type": "DOUBLE", "role": "metric"},
        ],
    },
]


# ---------------------------------------------------------------------------
# _gcs_auth_mode
# ---------------------------------------------------------------------------


class TestGcsAuthMode:
    def test_default_none(self, monkeypatch):
        monkeypatch.delenv("CLEAN_QUERY_GCS_AUTH", raising=False)
        assert catalog._gcs_auth_mode() is None

    def test_true_values(self, monkeypatch):
        for val in ("1", "true", "True", "yes", "YES"):
            monkeypatch.setenv("CLEAN_QUERY_GCS_AUTH", val)
            assert catalog._gcs_auth_mode() is True

    def test_false_values(self, monkeypatch):
        for val in ("0", "false", "False", "no", "NO"):
            monkeypatch.setenv("CLEAN_QUERY_GCS_AUTH", val)
            assert catalog._gcs_auth_mode() is False

    def test_unknown_value(self, monkeypatch):
        monkeypatch.setenv("CLEAN_QUERY_GCS_AUTH", "unknown")
        assert catalog._gcs_auth_mode() is None


# ---------------------------------------------------------------------------
# _glob_to_regex
# ---------------------------------------------------------------------------


class TestGlobToRegex:
    def test_literal_string(self):
        r = catalog._glob_to_regex("test.parquet")
        assert r.match("test.parquet")
        assert not r.match("testXparquet")

    def test_single_asterisk(self):
        r = catalog._glob_to_regex("test_*.parquet")
        assert r.match("test_2024.parquet")
        assert r.match("test_abc.parquet")
        assert not r.match("test_2024.csv")

    def test_path_with_asterisk(self):
        r = catalog._glob_to_regex("gs://bucket/*/file.parquet")
        assert r.match("gs://bucket/2024/file.parquet")
        assert r.match("gs://bucket/abc/file.parquet")

    def test_special_chars_escaped(self):
        r = catalog._glob_to_regex("test(1).parquet")
        assert r.match("test(1).parquet")
        assert not r.match("test1.parquet")

    def test_multi_asterisk(self):
        r = catalog._glob_to_regex("a/*/b/*/c.parquet")
        assert r.match("a/x/b/y/c.parquet")


# ---------------------------------------------------------------------------
# get_year_column
# ---------------------------------------------------------------------------


class TestGetYearColumn:
    def test_anno_integer(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.get_year_column("test_single")
        assert result == "anno"

    def test_anno_di_imposta(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.get_year_column("test_multi")
        assert result == "anno_di_imposta"

    def test_no_anno_column(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.get_year_column("test_no_anno")
        assert result is None

    def test_string_anno_skipped(self, monkeypatch):
        """Colonne VARCHAR non devono essere identificate come year column."""
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.get_year_column("test_string_anno")
        assert result is None

    def test_unknown_slug(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.get_year_column("nonexistent")
        assert result is None


# ---------------------------------------------------------------------------
# list_datasets
# ---------------------------------------------------------------------------


class TestListDatasets:
    def test_returns_all_datasets(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.list_datasets()
        assert len(result) == 4
        assert result[0]["slug"] == "test_single"
        assert result[1]["slug"] == "test_multi"

    def test_includes_correct_keys(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.list_datasets()
        entry = result[0]
        assert "slug" in entry
        assert "name" in entry
        assert "description" in entry
        assert "period_start" in entry
        assert "period_end" in entry

    def test_empty_catalog(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: [])
        result = catalog.list_datasets()
        assert result == []


# ---------------------------------------------------------------------------
# describe_dataset
# ---------------------------------------------------------------------------


class TestDescribeDataset:
    def test_valid_slug(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.describe_dataset("test_single")
        assert result["slug"] == "test_single"
        assert result["name"] == "Test Single"
        assert len(result["columns"]) == 2
        assert result["location_type"] == "local"

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.describe_dataset("nonexistent")
        assert "error" in result
        assert "non trovato" in result["error"]

    def test_shows_available_slugs(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.describe_dataset("nonexistent")
        assert "test_single" in result["error"]
        assert "test_multi" in result["error"]


# ---------------------------------------------------------------------------
# search_datasets
# ---------------------------------------------------------------------------


class TestSearchDatasets:
    def test_search_by_name(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("Single")
        assert len(result) == 1
        assert result[0]["slug"] == "test_single"

    def test_search_by_description(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("multi-anno")
        assert len(result) == 1
        assert result[0]["slug"] == "test_multi"

    def test_search_by_source(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("test_source")
        assert len(result) == 2

    def test_search_case_insensitive(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("SINGLE")
        assert len(result) == 1

    def test_no_match(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("nonexistent_xyz")
        assert result == []

    def test_empty_query(self, monkeypatch):
        monkeypatch.setattr(catalog, "_load_catalog", lambda: _SAMPLE_CATALOG)
        result = catalog.search_datasets("")
        assert len(result) == 4


# ---------------------------------------------------------------------------
# gcs_cache_stats / gcs_cache_clear
# ---------------------------------------------------------------------------


class TestGcsCache:
    def test_cache_clear(self):
        """gcs_cache_clear svuota la cache."""
        # Popola la cache con un entry
        catalog._gcs_res_cache[("test", 2023)] = (0.0, ["url1"])
        catalog.gcs_cache_clear()
        assert len(catalog._gcs_res_cache) == 0

    def test_cache_stats_empty(self):
        """Cache vuota -> statistiche zero."""
        catalog._gcs_res_cache.clear()
        stats = catalog.gcs_cache_stats()
        assert stats["total_entries"] == 0
        assert stats["valid_entries"] == 0

    def test_cache_stats_with_entries(self):
        """Cache con entry -> statistiche corrette."""
        import time

        now = time.time()
        catalog._gcs_res_cache.clear()
        catalog._gcs_res_cache[("ds1", 2023)] = (now, ["url1", "url2"])
        catalog._gcs_res_cache[("ds2", None)] = (now, ["url3"])
        stats = catalog.gcs_cache_stats()
        assert stats["total_entries"] == 2
        assert stats["valid_entries"] == 2
        assert len(stats["entries"]) == 2
        # Pulisci
        catalog._gcs_res_cache.clear()

    def test_cache_stats_fresh_expired(self, monkeypatch):
        """Entry scadute -> non conteggiate come valide."""
        catalog._gcs_res_cache.clear()
        import time

        old = time.time() - catalog._gcs_res_cache_ttl - 10
        catalog._gcs_res_cache[("old", 2020)] = (old, ["url"])
        stats = catalog.gcs_cache_stats()
        assert stats["total_entries"] == 1
        assert stats["valid_entries"] == 0
        assert stats["entries"][0]["fresh"] is False
        catalog._gcs_res_cache.clear()
