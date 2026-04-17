from __future__ import annotations

import argparse
import contextlib
import io
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from scaffold_candidate import scaffold  # noqa: E402


def run_scaffold(args: argparse.Namespace) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        return scaffold(args)


class ScaffoldCandidateTest(unittest.TestCase):
    def make_args(self, tmp_path: Path, *, write: bool = False) -> argparse.Namespace:
        return argparse.Namespace(
            slug="test-candidato",
            title="Test Candidato",
            discussion_url="https://github.com/dataciviclab/datasets/discussions/1",
            issue_url="https://github.com/dataciviclab/dataset-incubator/issues/1",
            source_url="https://example.com/data.csv",
            created_date="2026-04-17",
            template_dir=ROOT / "templates" / "candidate",
            candidates_dir=tmp_path / "candidates",
            write=write,
            force=False,
        )

    def test_dry_run_does_not_write_files(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            self.assertEqual(run_scaffold(self.make_args(tmp_path)), 0)

            self.assertFalse((tmp_path / "candidates" / "test-candidato").exists())

    def test_write_copies_template_and_replaces_placeholders(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            self.assertEqual(run_scaffold(self.make_args(tmp_path, write=True)), 0)

            candidate_dir = tmp_path / "candidates" / "test-candidato"
            self.assertTrue((candidate_dir / "dataset.yml").exists())
            self.assertTrue((candidate_dir / "notebooks" / "test-candidato_v0.ipynb").exists())

            readme = (candidate_dir / "README.md").read_text(encoding="utf-8")
            dataset = (candidate_dir / "dataset.yml").read_text(encoding="utf-8")
            self.assertIn("# Test Candidato", readme)
            self.assertIn("https://github.com/dataciviclab/dataset-incubator/issues/1", readme)
            self.assertIn("https://example.com/data.csv", dataset)
            self.assertIn('name: "test-candidato"', dataset)
            self.assertIn('name: "mart_test_candidato"', dataset)

    def test_existing_candidate_requires_force(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            args = self.make_args(tmp_path, write=True)
            self.assertEqual(run_scaffold(args), 0)

            with self.assertRaises(SystemExit):
                run_scaffold(args)


if __name__ == "__main__":
    unittest.main()
