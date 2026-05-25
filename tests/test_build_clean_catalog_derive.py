"""Tests per build_clean_catalog.py --derive.

Contratto: derive_catalog_from_gcs() produce un catalogo valido a partire
dai parquet su GCS. Mocka list_objects, object_exists e DuckDB.

Prova del fuoco: se cancello questi test, un refactor della logica di
derivazione puo' produrre cataloghi con slug mancanti o colonne errate.
"""

from __future__ import annotations

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
                    "period": {"start": 2023, "end": 2024},
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
    def test_derive_merges_editorial_metadata(self, mock_exists, mock_list, mock_connect):
        """Name, description, source, stage devono venire dal catalogo esistente."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import derive_catalog_from_gcs

        catalog, _ = derive_catalog_from_gcs(self.existing_catalog, refresh_date=False)
        ds = {d["slug"]: d for d in catalog["datasets"]}

        # test_slug_a esiste → preserva name, description, source, source_id, stage
        a = ds["test_slug_a"]
        self.assertEqual(a["name"], "Nome Umano")
        self.assertEqual(a["description"], "Descrizione esistente")
        self.assertEqual(a["source"], "Fonte Manuale")
        self.assertEqual(a["source_id"], "manual-id")
        self.assertEqual(a["stage"], "published")

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
    def test_main_derive_dry_run_exits_zero(self, mock_exists, mock_list, mock_connect):
        """--derive senza --write non deve crashare."""
        mock_connect.return_value = FakeDuckDBConnection()

        from scripts.build_clean_catalog import main
        import sys

        test_args = ["--derive", "--catalog", str(self.tmpdir / "catalog.json")]
        with patch.object(sys, "argv", ["build_clean_catalog.py"] + test_args):
            rc = main()
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
