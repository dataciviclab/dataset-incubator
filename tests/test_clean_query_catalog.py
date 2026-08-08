# ruff: noqa: E402
"""Test per validazione del registry contro lo schema JSON.

Contratto: validate_catalog() verifica che un artifact registry rispetti lo
schema JSON regolamentare. Usato in CI per validare registry.json (fusion ADR,
toolkit v1.49.0). La proiezione legacy clean_catalog.json resta per i consumer
non ancora migrati; il contratto canonico è registry.json.

Prova del fuoco: se cancello questi test, un catalogo malformato puo'
essere pubblicato senza preavviso.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[1]


def validate_catalog(catalog, _schema) -> list:
    """Valida contro lo schema condiviso del toolkit (fusion ADR, #453).

    Wrapper per il contratto storico del test (lista errori stringa).
    """
    from toolkit.registry.validation import validate_artifact

    return validate_artifact(catalog, "registry.schema.json")


@pytest.mark.contract
class CleanCatalogValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = None  # schema dal toolkit (validate_catalog)
        self.catalog = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))

    def test_current_catalog_matches_schema(self) -> None:
        self.assertEqual(validate_catalog(self.catalog, self.schema), [])

    def test_schema_rejects_invalid_slug(self) -> None:
        catalog = dict(self.catalog)
        dataset = dict(catalog["datasets"][0])
        dataset["slug"] = "Bad-Slug"
        catalog["datasets"] = [dataset]
        errors = validate_catalog(catalog, self.schema)
        self.assertTrue(any("does not match" in error for error in errors), errors)

    def test_schema_rejects_invalid_stage(self) -> None:
        catalog = dict(self.catalog)
        dataset = dict(catalog["datasets"][0])
        dataset["stage"] = "ready-ish"
        catalog["datasets"] = [dataset]
        errors = validate_catalog(catalog, self.schema)
        self.assertTrue(any("is not one of" in error for error in errors), errors)

    def test_schema_rejects_extra_location_property(self) -> None:
        catalog = dict(self.catalog)
        dataset = dict(catalog["datasets"][0])
        location = dict(dataset["location"])
        location["extra"] = "not allowed"
        dataset["location"] = location
        catalog["datasets"] = [dataset]
        errors = validate_catalog(catalog, self.schema)
        self.assertTrue(
            any("Additional properties are not allowed" in error for error in errors), errors
        )


class TestSearchByTag:
    """Contratto: search_datasets matcha per tag e category (oltre a nome/descrizione/fonte)."""

    @pytest.fixture(autouse=True)
    def _mock_catalog(self, monkeypatch):
        catalog = [
            {
                "slug": "demo_energia",
                "name": "Demo Energia",
                "description": "",
                "source": "",
                "period": {"start": 2020, "end": 2024},
                "columns": [{"name": "x", "type": "INTEGER", "role": "metric", "description": ""}],
                "location": {"type": "gcs", "path": "gs://b/x"},
                "tags": ["energia"],
                "category": "energia",
            },
            {
                "slug": "demo_no_tag",
                "name": "No Tag",
                "description": "",
                "source": "",
                "period": {"start": 2020, "end": 2024},
                "columns": [{"name": "x", "type": "INTEGER", "role": "metric", "description": ""}],
                "location": {"type": "gcs", "path": "gs://b/y"},
            },
        ]
        import tools.clean_query_mcp.catalog as cat

        monkeypatch.setattr(cat, "_load_catalog", lambda: catalog)

    def test_search_matches_by_tag(self):
        from tools.clean_query_mcp.catalog import search_datasets

        results = search_datasets("energia")
        slugs = [r["slug"] for r in results]
        assert "demo_energia" in slugs
        assert "demo_no_tag" not in slugs
