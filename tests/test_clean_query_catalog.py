"""Test per validazione catalogo clean contro schema JSON.

Contratto: validate_catalog() verifica che un catalogo rispetti lo schema
JSON regolamentare. Usato in CI per validare clean_catalog.json.

Prova del fuoco: se cancello questi test, un catalogo malformato puo'
essere pubblicato senza preavviso.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
from build_clean_catalog import validate_catalog


@pytest.mark.contract
class CleanCatalogValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(
            (ROOT / "registry" / "clean_catalog.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.catalog = json.loads(
            (ROOT / "registry" / "clean_catalog.json").read_text(encoding="utf-8")
        )

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
        self.assertTrue(any("not in enum" in error for error in errors), errors)

    def test_schema_rejects_extra_location_property(self) -> None:
        catalog = dict(self.catalog)
        dataset = dict(catalog["datasets"][0])
        location = dict(dataset["location"])
        location["extra"] = "not allowed"
        dataset["location"] = location
        catalog["datasets"] = [dataset]
        errors = validate_catalog(catalog, self.schema)
        self.assertTrue(any("additional property" in error for error in errors), errors)
