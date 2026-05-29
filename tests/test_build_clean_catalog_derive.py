"""Tests per build_clean_catalog.py --derive.

Contratto: derive_catalog_from_gcs() produce un catalogo valido a partire
dai parquet su GCS. Mocka list_objects, object_exists e DuckDB.

Prova del fuoco: se cancello questi test, un refactor della logica di
derivazione puo' produrre cataloghi con slug mancanti o colonne errate.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

FAKE_PARQUET_OBJECTS = [
    {"name": "test_slug_a/2023/test_slug_a_2023_clean.parquet"},
    {"name": "test_slug_a/2024/test_slug_a_2024_clean.parquet"},
    {"name": "test_slug_b/2024/test_slug_b_2024_clean.parquet"},
    {"name": "test_slug_c/2024/test_slug_c_2024_clean.parquet"},  # no pipeline_run
]

def fake_list_objects(bucket, **kw):
    return FAKE_PARQUET_OBJECTS

def fake_object_exists(bucket, key):
    # Solo test_slug_a e test_slug_b hanno pipeline_run.json
    if "pipeline_run" in key:
        return key.startswith("test_slug_a/") or key.startswith("test_slug_b/")
    return True  # per i parquet, esistono tutti

# DuckDB mock che ritorna schema prevedibile
MOCK_DESCRIBE_ROWS = [
    ("anno", "INTEGER", "YES", None, None, None),
    ("nome", "VARCHAR", "YES", None, None, None),
    ("valore", "DOUBLE", "YES", None, None, None),
]


class FakeDuckDBConnection:
    def sql(self, query):
        return self
    def fetchall(self):
        return MOCK_DESCRIBE_ROWS
    def close(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass


@pytest.mark.contract
class TestBuildCleanCatalogDerive(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.maxDiff = None
        # Usa un catalogo editoriale fittizio per testare il merge
        self.existing_catalog = {
            "schema_version": 1,
            "updated_at": "2026-01-01",
            "datasets": [
                {
                    "slug": "test_slug_a",
                    "name": "Nome Umano",
                    "description": "Descrizione esistente",
                    "source": "Fonte Manuale",
                    "source_id": "manual-id",
                    "period": {"start": 2020, "end": 2025},  # piu' ampio del GCS (2023-2024)
                    "columns": [
                        {"name": "anno", "type": "INTEGER", "role": "dimension", "description": "Anno di riferimento"},
                        {"name": "nome", "type": "VARCHAR", "role": "dimension", "description": "Nome del dataset"},
                    ],
                    "location": {"type": "gcs", "path": "gs://bucket/test_slug_a/*/test_slug_a_*_clean.parquet", "multi_file": True},
                    "stage": "published",
                    "registry_source": "manual",
                }
            ],
        }
        self.tmpdir = Path("/tmp/test_build_clean_catalog_derive")

    def _run_derive(self, args: list[str], expect_zero: bool = True) -> int:
        """Helper: esegui build_clean_catalog.py --derive con mock."""
        # The function is in __main__ context, call main() directly
        # Actually we need to mock at module level before import
        # Better: call derive_catalog_from_gcs directly
        pass

    # ── Test derive_catalog_from_gcs ────────────────────────────────────────

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_filters_without_pipeline_run(self, mock_exists, mock_list, mock_connect):
        """Slug senza pipeline_run.json devono essere esclusi."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, errors = derive_catalog_from_gcs({"datasets": []}, refresh_date=False)

        slugs = [d["slug"] for d in catalog["datasets"]]
        self.assertIn("test_slug_a", slugs)
        self.assertIn("test_slug_b", slugs)
        self.assertNotIn("test_slug_c", slugs)  # no pipeline_run
        self.assertEqual(errors, [])

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_merges_editorial_metadata(self, mock_exists, mock_list, mock_connect):
        """Name, description, source, stage, period devono venire dal catalogo esistente."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs(self.existing_catalog, refresh_date=False)
        ds = {d["slug"]: d for d in catalog["datasets"]}

        # test_slug_a esiste → preserva name, description, source, source_id, stage, period
        a = ds["test_slug_a"]
        self.assertEqual(a["name"], "Nome Umano")
        self.assertEqual(a["description"], "Descrizione esistente")
        self.assertEqual(a["source"], "Fonte Manuale")
        self.assertEqual(a["source_id"], "manual-id")
        self.assertEqual(a["stage"], "published")
        self.assertEqual(a["period"], {"start": 2020, "end": 2025})  # editoriale, non dal path GCS

        # test_slug_b è nuovo → defaults
        b = ds["test_slug_b"]
        self.assertEqual(b["name"], "Test Slug B")  # title()
        self.assertEqual(b["stage"], "published")

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.regression
    def test_derive_preserves_column_metadata(self, mock_exists, mock_list, mock_connect):
        """description e role delle colonne devono venire dall'editoriale, type dal parquet."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs(self.existing_catalog, refresh_date=False)
        ds = {d["slug"]: d for d in catalog["datasets"]}

        # test_slug_a ha colonne editoriali → preserve description e role
        a = ds["test_slug_a"]
        cols = {c["name"]: c for c in a["columns"]}

        # anno: role diverso tra editoriale (dimension) e derive (metric → INTEGER)
        self.assertEqual(cols["anno"]["role"], "dimension")        # da editoriale
        self.assertEqual(cols["anno"]["description"], "Anno di riferimento")  # da editoriale
        self.assertEqual(cols["anno"]["type"], "INTEGER")          # dal parquet

        # nome: uguale in editoriale e derive
        self.assertEqual(cols["nome"]["role"], "dimension")
        self.assertEqual(cols["nome"]["description"], "Nome del dataset")
        self.assertEqual(cols["nome"]["type"], "VARCHAR")

        # valore: colonna nuova (solo parquet) → defaults derive
        self.assertEqual(cols["valore"]["role"], "metric")
        self.assertEqual(cols["valore"]["description"], "")
        self.assertEqual(cols["valore"]["type"], "DOUBLE")

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_preserves_columns(self, mock_exists, mock_list, mock_connect):
        """Le colonne devono essere derivate dal parquet."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs({"datasets": []}, refresh_date=False)
        a = catalog["datasets"][0]
        col_names = [c["name"] for c in a["columns"]]
        self.assertEqual(col_names, ["anno", "nome", "valore"])

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_preserves_column_types(self, mock_exists, mock_list, mock_connect):
        """BIGINT, INTEGER, DOUBLE, VARCHAR devono essere preservati dal parquet."""
        mock_rows = [
            ("id_big", "BIGINT", "YES", None, None, None),
            ("id_int", "INTEGER", "YES", None, None, None),
            ("valore", "DOUBLE", "YES", None, None, None),
            ("nome", "VARCHAR", "YES", None, None, None),
            ("data", "DATE", "YES", None, None, None),
            ("attivo", "BOOLEAN", "YES", None, None, None),
        ]

        class FakeTypeConnection:
            def sql(self, query): return self
            def fetchall(self): return mock_rows
            def close(self): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass

        mock_connect.return_value = FakeTypeConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs({"datasets": []}, refresh_date=False)
        cols = {c["name"]: c for c in catalog["datasets"][0]["columns"]}

        self.assertEqual(cols["id_big"]["type"], "BIGINT")
        self.assertEqual(cols["id_int"]["type"], "INTEGER")
        self.assertEqual(cols["valore"]["type"], "DOUBLE")
        self.assertEqual(cols["nome"]["type"], "VARCHAR")
        self.assertEqual(cols["data"]["type"], "DATE")
        self.assertEqual(cols["attivo"]["type"], "BOOLEAN")

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_multi_file_vs_single(self, mock_exists, mock_list, mock_connect):
        """Multi-file se ha più anni, single se un anno solo."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs({"datasets": []}, refresh_date=False)
        ds = {d["slug"]: d for d in catalog["datasets"]}
        self.assertTrue(ds["test_slug_a"]["location"]["multi_file"])  # 2 years
        self.assertFalse(ds["test_slug_b"]["location"]["multi_file"])  # 1 year

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_derive_schema_error_returns_errors(self, mock_exists, mock_list, mock_connect):
        """Se DuckDB fallisce, l'errore deve essere ritornato."""
        mock_conn = MagicMock()
        mock_conn.sql.side_effect = Exception("DuckDB exploded")
        mock_conn.__enter__.return_value = mock_conn  # context manager → stesso oggetto
        mock_connect.return_value = mock_conn

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, errors = derive_catalog_from_gcs({"datasets": []}, refresh_date=False)
        self.assertEqual(len(catalog["datasets"]), 0)  # tutti falliti
        self.assertGreater(len(errors), 0)
        self.assertIn("DuckDB exploded", errors[0])

    # ── Test CLI dry-run (--derive senza --write) ───────────────────────────

    @patch("duckdb.connect")
    @patch("scripts.build_clean_catalog.list_objects", side_effect=fake_list_objects)
    @patch("scripts.build_clean_catalog.object_exists", side_effect=fake_object_exists)
    @pytest.mark.contract
    def test_main_derive_dry_run_exits_zero(self, mock_exists, mock_list, mock_connect):
        """--derive senza --write non deve crashare."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import main
        import sys

        test_args = ["--derive", "--catalog", str(self.tmpdir / "catalog.json")]
        with patch.object(sys, "argv", ["build_clean_catalog.py"] + test_args):
            rc = main()
            self.assertEqual(rc, 0)


# ---------------------------------------------------------------------------
# Tests per _enrich_period_from_coverage
# ---------------------------------------------------------------------------


@pytest.mark.contract
class TestEnrichPeriodFromCoverage(unittest.TestCase):
    """time_coverage nei dataset.yml deve sovrascrivere period nel catalogo."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.candidates_dir = self.tmpdir / "candidates"
        self.candidates_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_candidate(self, slug: str, start_year: int | None = None, end_year: int | None = None) -> Path:
        cand_dir = self.candidates_dir / slug
        cand_dir.mkdir(exist_ok=True)
        yml = cand_dir / "dataset.yml"
        lines = [f'dataset:', f'  name: "{slug}"', f'  years: [2024]']
        if start_year is not None:
            lines.append("  time_coverage:")
            lines.append(f"    start_year: {start_year}")
            lines.append(f"    end_year: {end_year}")
        lines.append("")
        yml.write_text("\n".join(lines))
        return yml

    def _make_catalog_entry(self, slug: str, period_start: int = 2024, period_end: int = 2024) -> dict:
        return {
            "slug": slug,
            "name": slug.replace("_", " ").title(),
            "description": "",
            "source": "",
            "period": {"start": period_start, "end": period_end},
            "columns": [{"name": "x", "type": "INTEGER", "role": "metric", "description": ""}],
            "location": {"type": "gcs", "path": f"gs://bucket/{slug}/2024/{slug}_2024_clean.parquet", "multi_file": False},
        }

    def test_overrides_period_from_coverage(self):
        """time_coverage.start_year/end_year deve sovrascrivere period."""
        self._make_candidate("test_slug_x", start_year=2010, end_year=2024)
        catalog = {"datasets": [self._make_catalog_entry("test_slug_x", period_start=2024, period_end=2024)]}

        from scripts.build_clean_catalog import _enrich_period_from_coverage
        _enrich_period_from_coverage(catalog, self.tmpdir)

        ds = catalog["datasets"][0]
        self.assertEqual(ds["period"]["start"], 2010)
        self.assertEqual(ds["period"]["end"], 2024)

    def test_ignores_candidate_without_coverage(self):
        """Candidato senza time_coverage non altera period."""
        self._make_candidate("test_slug_x")  # no time_coverage
        catalog = {"datasets": [self._make_catalog_entry("test_slug_x", period_start=2024, period_end=2024)]}

        from scripts.build_clean_catalog import _enrich_period_from_coverage
        _enrich_period_from_coverage(catalog, self.tmpdir)

        ds = catalog["datasets"][0]
        self.assertEqual(ds["period"]["start"], 2024)  # invariato
        self.assertEqual(ds["period"]["end"], 2024)

    def test_ignores_unrelated_slug(self):
        """Slug non presente nei candidati non viene alterato."""
        self._make_candidate("test_slug_a", start_year=2010, end_year=2024)
        catalog = {"datasets": [self._make_catalog_entry("test_slug_b", period_start=2020, period_end=2020)]}

        from scripts.build_clean_catalog import _enrich_period_from_coverage
        _enrich_period_from_coverage(catalog, self.tmpdir)

        ds = catalog["datasets"][0]
        self.assertEqual(ds["period"]["start"], 2020)  # invariato

    def test_multiple_candidates(self):
        """Due candidati con time_coverage vengono entrambi aggiornati."""
        self._make_candidate("alpha", start_year=2000, end_year=2010)
        self._make_candidate("beta", start_year=2011, end_year=2020)
        catalog = {
            "datasets": [
                self._make_catalog_entry("alpha", period_start=2000, period_end=2000),
                self._make_catalog_entry("beta", period_start=2011, period_end=2011),
                self._make_catalog_entry("gamma"),  # senza candidate dir
            ]
        }

        from scripts.build_clean_catalog import _enrich_period_from_coverage
        _enrich_period_from_coverage(catalog, self.tmpdir)

        by_slug = {d["slug"]: d for d in catalog["datasets"]}
        self.assertEqual(by_slug["alpha"]["period"], {"start": 2000, "end": 2010})
        self.assertEqual(by_slug["beta"]["period"], {"start": 2011, "end": 2020})
        self.assertEqual(by_slug["gamma"]["period"], {"start": 2024, "end": 2024})  # invariato


if __name__ == "__main__":
    unittest.main()
