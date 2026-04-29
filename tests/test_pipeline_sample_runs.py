from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_pipeline_sample_runs import apply_sample_results, summarize_sample_results  # noqa: E402


class PipelineSampleRunTest(unittest.TestCase):
    def test_single_sample_result_uses_flat_shape(self) -> None:
        summary = summarize_sample_results(
            [
                {
                    "id": "istat-housing-crowding",
                    "status": "passed",
                    "year": 2024,
                    "config_path": "candidates/istat-housing-crowding/dataset.yml",
                    "run_id": "123",
                    "run_url": "https://example.test/runs/123",
                    "checked_at": "2026-04-29",
                }
            ]
        )

        self.assertEqual(summary["status"], "passed")
        self.assertEqual(summary["year"], 2024)
        self.assertEqual(
            summary["config_path"],
            "candidates/istat-housing-crowding/dataset.yml",
        )
        self.assertNotIn("configs", summary)

    def test_multiple_sample_results_are_aggregated(self) -> None:
        summary = summarize_sample_results(
            [
                {
                    "id": "multi",
                    "status": "passed",
                    "year": 2023,
                    "config_path": "candidates/multi/sources/a/dataset.yml",
                    "run_id": "123",
                    "run_url": "https://example.test/runs/123",
                    "checked_at": "2026-04-29",
                },
                {
                    "id": "multi",
                    "status": "failed",
                    "year": 2024,
                    "config_path": "candidates/multi/sources/b/dataset.yml",
                    "run_id": "123",
                    "run_url": "https://example.test/runs/123",
                    "checked_at": "2026-04-29",
                },
            ]
        )

        self.assertEqual(summary["status"], "failed")
        self.assertEqual(summary["years"], [2023, 2024])
        self.assertEqual(len(summary["configs"]), 2)

    def test_apply_sample_results_updates_matching_signal(self) -> None:
        catalog = {
            "signals": [
                {
                    "id": "bdap-anagrafe-enti",
                    "status": "ok",
                    "label": "bdap-anagrafe-enti",
                    "detail": "",
                    "action": "",
                }
            ]
        }

        errors = apply_sample_results(
            catalog,
            [
                {
                    "id": "bdap-anagrafe-enti",
                    "status": "passed",
                    "year": 2024,
                    "config_path": "support_datasets/bdap-anagrafe-enti/dataset.yml",
                    "run_id": "123",
                    "run_url": "https://example.test/runs/123",
                    "checked_at": "2026-04-29",
                }
            ],
        )

        self.assertEqual(errors, [])
        self.assertEqual(catalog["signals"][0]["sample_run"]["status"], "passed")

    def test_apply_sample_results_rejects_unknown_signal(self) -> None:
        catalog = {"signals": []}

        errors = apply_sample_results(catalog, [{"id": "missing"}])

        self.assertEqual(errors, ["missing: no matching signal in catalog"])


if __name__ == "__main__":
    unittest.main()
