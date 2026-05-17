from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from update_pipeline_sample_runs import apply_sample_results, summarize_sample_results  # noqa: E402

_SCHEMA_PATH = ROOT / "registry" / "pipeline_signals.schema.json"


def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


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
        self.assertEqual(summary["years"], [2024])
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


class PipelineSignalsSchemaTest(unittest.TestCase):
    """Validate pipeline_signals.json against its JSON Schema."""

    def test_live_artifact_complies_with_schema(self) -> None:
        """Il pipeline_signals.json committato deve rispettare lo schema."""
        artifact_path = ROOT / "registry" / "pipeline_signals.json"
        self.assertTrue(artifact_path.exists(), "pipeline_signals.json not found")
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        schema = _load_schema()
        jsonschema.validate(instance=payload, schema=schema)

    def test_minimal_signals_payload_complies(self) -> None:
        """Un payload minimale con un segnale senza sample_run deve essere valido."""
        payload = {
            "schema_version": "1",
            "generated_at": "2026-05-17",
            "repo": "dataset-incubator",
            "topic": "pipeline_state",
            "summary": {"total": 1, "by_status": {"ok": 1, "warn": 0, "error": 0}},
            "signals": [
                {
                    "id": "test-candidate",
                    "status": "ok",
                    "label": "test-candidate",
                    "detail": "test — fonte test",
                    "action": "",
                }
            ],
        }
        schema = _load_schema()
        jsonschema.validate(instance=payload, schema=schema)

    def test_signal_with_single_year_sample_run(self) -> None:
        """Segnale con sample_run single-year."""
        payload = {
            "schema_version": "1",
            "generated_at": "2026-05-17",
            "repo": "dataset-incubator",
            "topic": "pipeline_state",
            "summary": {"total": 1, "by_status": {"ok": 1, "warn": 0, "error": 0}},
            "signals": [
                {
                    "id": "test-candidate",
                    "source_id": "test_source",
                    "status": "ok",
                    "label": "test-candidate",
                    "detail": "anno 2024 — fonte test_csv — mart: sì",
                    "action": "",
                    "sample_run": {
                        "status": "passed",
                        "run_id": "123",
                        "run_url": "https://github.com/test/actions/runs/123",
                        "checked_at": "2026-05-07",
                        "year": 2024,
                        "config_path": "candidates/test-candidate/dataset.yml",
                    },
                }
            ],
        }
        schema = _load_schema()
        jsonschema.validate(instance=payload, schema=schema)

    def test_signal_with_multi_year_sample_run(self) -> None:
        """Segnale con sample_run multi-year."""
        payload = {
            "schema_version": "1",
            "generated_at": "2026-05-17",
            "repo": "dataset-incubator",
            "topic": "pipeline_state",
            "summary": {"total": 1, "by_status": {"ok": 1, "warn": 0, "error": 0}},
            "signals": [
                {
                    "id": "test-candidate",
                    "status": "ok",
                    "label": "test-candidate",
                    "detail": "anni 2023-2025 — fonte test_csv — mart: sì",
                    "action": "",
                    "sample_run": {
                        "status": "passed",
                        "run_id": "123",
                        "run_url": "https://github.com/test/actions/runs/123",
                        "checked_at": "2026-05-07",
                        "years": [2023, 2024, 2025],
                        "config_path": "candidates/test-candidate/dataset.yml",
                    },
                }
            ],
        }
        schema = _load_schema()
        jsonschema.validate(instance=payload, schema=schema)

    def test_signal_with_configs_sample_run(self) -> None:
        """Segnale con sample_run multi-config (post-merge multi-anno)."""
        payload = {
            "schema_version": "1",
            "generated_at": "2026-05-17",
            "repo": "dataset-incubator",
            "topic": "pipeline_state",
            "summary": {"total": 1, "by_status": {"ok": 1, "warn": 0, "error": 0}},
            "signals": [
                {
                    "id": "test-candidate",
                    "status": "ok",
                    "label": "test-candidate",
                    "detail": "anni 2023-2025 — fonte test_csv — mart: sì",
                    "action": "",
                    "sample_run": {
                        "status": "passed",
                        "run_id": "123",
                        "run_url": "https://github.com/test/actions/runs/123",
                        "checked_at": "2026-05-07",
                        "years": [2023, 2024, 2025],
                        "configs": [
                            {
                                "status": "passed",
                                "year": 2023,
                                "config_path": "candidates/test-candidate/dataset.yml",
                            },
                            {
                                "status": "passed",
                                "year": 2024,
                                "config_path": "candidates/test-candidate/dataset.yml",
                            },
                            {
                                "status": "failed",
                                "year": 2025,
                                "config_path": "candidates/test-candidate/dataset.yml",
                                "config_exists": False,
                            },
                        ],
                    },
                }
            ],
        }
        schema = _load_schema()
        jsonschema.validate(instance=payload, schema=schema)


if __name__ == "__main__":
    unittest.main()
