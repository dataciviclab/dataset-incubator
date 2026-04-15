from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_clean_catalog import validate_catalog  # noqa: E402


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

    def test_schema_rejects_invalid_status(self) -> None:
        catalog = dict(self.catalog)
        dataset = dict(catalog["datasets"][0])
        dataset["status"] = "ready-ish"
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


if __name__ == "__main__":
    unittest.main()
