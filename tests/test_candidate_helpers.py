"""Tests for _candidate_helpers shared helpers."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _candidate_helpers import (  # noqa: E402
    candidate_slug_from_path,
    is_nested_config,
    resolve_sample_year,
    resolve_support_entries,
    resolve_years,
)


def _write_dataset(tmp: Path, rel_path: str, content: str) -> Path:
    """Write a dataset.yml file inside tmp directory, return full path."""
    full = tmp / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    return full


class ResolveYearsTest(unittest.TestCase):
    """Tests for resolve_years() and resolve_sample_year()."""

    def test_valid_years(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
  years: [2020, 2021, 2024]
""")
            self.assertEqual(resolve_years(cfg), [2020, 2021, 2024])
            self.assertEqual(resolve_sample_year(cfg), 2024)

    def test_single_year(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
  years: [2022]
""")
            self.assertEqual(resolve_years(cfg), [2022])
            self.assertEqual(resolve_sample_year(cfg), 2022)

    def test_empty_years(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
  years: []
""")
            self.assertEqual(resolve_years(cfg), [])
            self.assertEqual(resolve_sample_year(cfg), 0)

    def test_missing_years_key(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
""")
            self.assertEqual(resolve_years(cfg), [])

    def test_missing_dataset_section(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", "raw: {}")
            self.assertEqual(resolve_years(cfg), [])

    def test_file_not_found(self) -> None:
        self.assertEqual(resolve_years(Path("/nonexistent/dataset.yml")), [])

    def test_years_not_sorted(self) -> None:
        """Years should be sorted in output regardless of input order."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
  years: [2024, 2020, 2022]
""")
            self.assertEqual(resolve_years(cfg), [2020, 2022, 2024])
            self.assertEqual(resolve_sample_year(cfg), 2024)

    def test_years_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", """
dataset:
  name: Test
  years: [not_a_number]
""")
            self.assertEqual(resolve_years(cfg), [])

    def test_yaml_parse_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            cfg = _write_dataset(tmp, "dataset.yml", "invalid: [yaml: bad")
            self.assertEqual(resolve_years(cfg), [])


class ResolveSupportEntriesTest(unittest.TestCase):
    """Tests for resolve_support_entries()."""

    def test_root_level_support(self) -> None:
        root = Path("/repo")
        cfg = {
            "support": [
                {"name": "Base Dataset", "config": "support/basic/dataset.yml", "years": [2023]},
            ],
        }
        entries = resolve_support_entries(cfg, Path("/repo/candidates/mine"), root)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["name"], "Base Dataset")
        self.assertEqual(entries[0]["years"], [2023])

    def test_dataset_level_support(self) -> None:
        root = Path("/repo")
        cfg = {
            "dataset": {
                "support": [
                    {"name": "Ref Data", "config": "support/ref/dataset.yml", "years": [2022]},
                ],
            },
        }
        entries = resolve_support_entries(cfg, Path("/repo/candidates/mine"), root)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["name"], "Ref Data")

    def test_both_levels_combined(self) -> None:
        root = Path("/repo")
        cfg = {
            "support": [
                {"name": "Root Support", "config": "support/root/dataset.yml", "years": [2023]},
            ],
            "dataset": {
                "support": [
                    {"name": "Dataset Support", "config": "support/ds/dataset.yml", "years": [2024]},
                ],
            },
        }
        entries = resolve_support_entries(cfg, Path("/repo/candidates/mine"), root)
        self.assertEqual(len(entries), 2)

    def test_no_support_returns_empty(self) -> None:
        entries = resolve_support_entries({}, Path("/repo/candidates/mine"), Path("/repo"))
        self.assertEqual(entries, [])

    def test_empty_config_field_skipped(self) -> None:
        cfg = {
            "support": [
                {"name": "No Config", "config": "", "years": []},
            ],
        }
        entries = resolve_support_entries(cfg, Path("/repo/candidates/mine"), Path("/repo"))
        self.assertEqual(entries, [])

    def test_path_resolved_relative_to_root(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            root = tmp
            cfg_path = tmp / "candidates" / "mine" / "dataset.yml"
            cfg_path.parent.mkdir(parents=True)
            cfg_path.write_text("dataset:\n  name: Test\n")

            # Create the support target
            support_path = tmp / "support" / "basic" / "dataset.yml"
            support_path.parent.mkdir(parents=True)
            support_path.write_text("dataset:\n  name: Support\n")

            cfg = {
                "support": [
                    {"name": "Basic", "config": "../../support/basic/dataset.yml", "years": [2023]},
                ],
            }
            entries = resolve_support_entries(cfg, cfg_path.parent, root)
            self.assertEqual(len(entries), 1)
            self.assertIn("support/basic/dataset.yml", entries[0]["config"])


class CandidateSlugFromPathTest(unittest.TestCase):
    """Tests for candidate_slug_from_path()."""

    def setUp(self) -> None:
        self.root = Path("/repo")

    def test_simple_candidate(self) -> None:
        path = Path("/repo/candidates/istat-housing-crowding/dataset.yml")
        self.assertEqual(candidate_slug_from_path(path, self.root), "istat-housing-crowding")

    def test_nested_multi_source(self) -> None:
        path = Path("/repo/candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml")
        self.assertEqual(candidate_slug_from_path(path, self.root), "ispra-ru-costi-kg")

    def test_support_dataset(self) -> None:
        path = Path("/repo/support_datasets/bdap-anagrafe-enti/dataset.yml")
        self.assertEqual(candidate_slug_from_path(path, self.root), "bdap-anagrafe-enti")

    def test_path_outside_root(self) -> None:
        path = Path("/other/candidates/test/dataset.yml")
        # Fallback to parent directory
        self.assertEqual(candidate_slug_from_path(path, self.root), "test")

    def test_short_path(self) -> None:
        path = Path("dataset.yml")
        self.assertIsNone(candidate_slug_from_path(path, self.root))


class IsNestedConfigTest(unittest.TestCase):
    """Tests for is_nested_config()."""

    def test_flat_single_source(self) -> None:
        self.assertFalse(is_nested_config(Path("/repo/candidates/test/dataset.yml")))

    def test_sources_nested(self) -> None:
        self.assertTrue(is_nested_config(Path("/repo/candidates/test/sources/a/dataset.yml")))

    def test_compose_nested(self) -> None:
        self.assertTrue(is_nested_config(Path("/repo/candidates/test/compose/dataset.yml")))

    def test_sources_in_other_context(self) -> None:
        """sources in a parent directory name should not trigger false positive."""
        self.assertFalse(is_nested_config(Path("/repo/sources_other/dataset.yml")))

    def test_support_dataset_flat(self) -> None:
        self.assertFalse(is_nested_config(Path("/repo/support_datasets/test/dataset.yml")))


if __name__ == "__main__":
    unittest.main()
