# ruff: noqa: E402
"""Test per scripts/build_registry.py — wrapper fusion del registry.

Contratto: il wrapper produce registry.json unico (fusion ADR) e scrive le
proiezioni legacy clean_catalog/pipeline_signals/entity_graph per i consumer
non ancora migrati. La logica di derivazione è del toolkit; qui si testa il
layout DI (existing preservato, proiezioni compatibili, exit codes).

Prova del fuoco: se cancello questi test, un wrapper rotto pubblica un
registry malformato o perde i metadata editoriali senza preavviso.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

import build_registry as br  # noqa: E402  (conftest aggiunge scripts/ al path)


def _registry_payload(**overrides) -> dict:
    """Payload minimo di build_registry del toolkit (fusion)."""
    payload = {
        "schema_version": 1,
        "repo": "dataset-incubator",
        "source_repo": "dataciviclab/dataset-incubator",
        "updated_at": "2026-08-08",
        "datasets": [
            {
                "slug": "demo_ds",
                "name": "Demo DS",
                "description": "Descrizione demo",
                "source": "Fonte demo",
                "period": {"start": 2020, "end": 2024},
                "columns": [
                    {
                        "name": "anno",
                        "type": "INTEGER",
                        "role": "dimension",
                        "semantic_type": "year",
                    }
                ],
                "location": {"type": "gcs", "path": "gs://dataciviclab-clean/demo_ds/"},
            }
        ],
        "marts": [{"name": "demo_ds__demo_mart", "parent_clean": "demo_ds"}],
        "signals": [
            {"id": "demo_ds", "status": "ok", "label": "demo_ds", "detail": "ok", "action": ""}
        ],
        "codelists": {"geo": {"name": "geo", "rows": 3}},
        "entities": {
            "generated_from": "registry.json",
            "entities": {"Comune": {"entity": "Comune", "label": "Comune (ISTAT)", "datasets": []}},
            "bridges": [],
            "summary": {"total_entities": 1, "total_relations": 0},
        },
        "summary": {"datasets": 1, "marts": 1, "signals": 1},
    }
    payload.update(overrides)
    return payload


def _result(**overrides) -> dict:
    """Risultato di build_registry: {"registry": ..., "errors": {...}}."""
    errors = {
        "datasets": {"derive": [], "validation": []},
        "marts": {"derive": [], "validation": []},
        "signals": {"derive": [], "validation": []},
        "codelists": {"derive": [], "validation": []},
        "entities": {"derive": [], "validation": []},
        "registry": {"derive": [], "validation": []},
    }
    return {"registry": _registry_payload(), "errors": errors, **overrides}


# ---------------------------------------------------------------------------
# _load_existing
# ---------------------------------------------------------------------------


class TestLoadExisting:
    def test_no_files_returns_none(self, tmp_path: Path) -> None:
        catalog, signals = br._load_existing(tmp_path)
        assert catalog is None
        assert signals is None

    def test_registry_json_priority(self, tmp_path: Path) -> None:
        (tmp_path / "registry.json").write_text(
            json.dumps({"datasets": [{"slug": "a"}], "signals": [{"id": "a"}]}),
            encoding="utf-8",
        )
        (tmp_path / "clean_catalog.json").write_text(
            json.dumps({"datasets": [{"slug": "legacy"}]}), encoding="utf-8"
        )
        catalog, signals = br._load_existing(tmp_path)
        assert catalog == {"datasets": [{"slug": "a"}]}
        assert signals == {"signals": [{"id": "a"}]}

    def test_registry_corrupt_falls_back_to_legacy(self, tmp_path: Path) -> None:
        (tmp_path / "registry.json").write_text("{not json", encoding="utf-8")
        (tmp_path / "clean_catalog.json").write_text(
            json.dumps({"datasets": [{"slug": "legacy"}]}), encoding="utf-8"
        )
        (tmp_path / "pipeline_signals.json").write_text(
            json.dumps({"signals": [{"id": "legacy"}]}), encoding="utf-8"
        )
        catalog, signals = br._load_existing(tmp_path)
        assert catalog == {"datasets": [{"slug": "legacy"}]}
        assert signals == {"signals": [{"id": "legacy"}]}

    def test_legacy_only(self, tmp_path: Path) -> None:
        (tmp_path / "clean_catalog.json").write_text(
            json.dumps({"datasets": [{"slug": "x"}]}), encoding="utf-8"
        )
        catalog, signals = br._load_existing(tmp_path)
        assert catalog == {"datasets": [{"slug": "x"}]}
        assert signals is None


# ---------------------------------------------------------------------------
# Proiezioni legacy
# ---------------------------------------------------------------------------


class TestProjections:
    def test_clean_catalog_header_preserved(self, tmp_path: Path) -> None:
        (tmp_path / "clean_catalog.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "name": "Nome Editoriale",
                    "description": "Descrizione editoriale",
                    "source_repo": "dataciviclab/dataset-incubator",
                    "updated_at": "2026-01-01",
                }
            ),
            encoding="utf-8",
        )
        registry = _registry_payload()
        proj = br._project_clean_catalog(registry, tmp_path)
        assert proj["name"] == "Nome Editoriale"
        assert proj["description"] == "Descrizione editoriale"
        assert proj["datasets"] == registry["datasets"]

    def test_clean_catalog_default_header(self, tmp_path: Path) -> None:
        proj = br._project_clean_catalog(_registry_payload(), tmp_path)
        assert proj["name"] == "Lab Clean Registry"
        assert proj["source_repo"] == "dataciviclab/dataset-incubator"
        assert len(proj["datasets"]) == 1

    def test_pipeline_signals_by_status(self, tmp_path: Path) -> None:
        registry = _registry_payload(
            signals=[
                {"id": "a", "status": "ok", "label": "a", "detail": "", "action": ""},
                {"id": "b", "status": "warn", "label": "b", "detail": "", "action": ""},
                {"id": "c", "status": "error", "label": "c", "detail": "", "action": ""},
            ]
        )
        proj = br._project_pipeline_signals(registry, tmp_path)
        assert proj["summary"] == {"total": 3, "by_status": {"ok": 1, "warn": 1, "error": 1}}

    def test_pipeline_signals_header_preserved(self, tmp_path: Path) -> None:
        (tmp_path / "pipeline_signals.json").write_text(
            json.dumps({"schema_version": "1", "repo": "dataset-incubator", "topic": "custom"}),
            encoding="utf-8",
        )
        proj = br._project_pipeline_signals(_registry_payload(), tmp_path)
        assert proj["repo"] == "dataset-incubator"
        assert proj["topic"] == "custom"

    def test_entity_graph_structure(self) -> None:
        proj = br._project_entity_graph(_registry_payload())
        assert proj["schema_version"] == 1
        assert proj["generated_from"] == "registry.json"
        assert "Comune" in proj["entities"]
        assert proj["bridges"] == []
        assert proj["summary"]["total_entities"] == 1

    def test_legacy_header_missing_file(self, tmp_path: Path) -> None:
        assert br._legacy_header(("schema_version", "name"), tmp_path / "missing.json", {}) == {}


# ---------------------------------------------------------------------------
# main() — exit codes e scrittura
# ---------------------------------------------------------------------------


@pytest.fixture
def patch_builder(monkeypatch: pytest.MonkeyPatch):
    """Sostituisce build_registry del toolkit con un fake controllato."""
    calls: dict[str, object] = {}

    def fake_build_registry(layout, *, derive_mode="local", **kwargs):
        calls["derive_mode"] = derive_mode
        calls["kwargs"] = kwargs
        return _result()

    monkeypatch.setattr("toolkit.registry.builders.build_registry", fake_build_registry)
    return calls


class TestMain:
    @pytest.fixture(autouse=True)
    def _isolate_argv(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("sys.argv", ["build_registry.py"])

    def test_dry_run_no_write(self, tmp_path: Path, patch_builder, _isolate_argv) -> None:
        sys.argv = ["build_registry.py", "--out", str(tmp_path)]
        code = br.main()
        assert code == 0
        assert not (tmp_path / "registry.json").exists()

    def test_write_produces_four_artifacts(
        self, tmp_path: Path, patch_builder, _isolate_argv
    ) -> None:
        sys.argv = ["build_registry.py", "--out", str(tmp_path), "--write"]
        code = br.main()
        assert code == 0
        for name in (
            "registry.json",
            "clean_catalog.json",
            "pipeline_signals.json",
            "entity_graph.json",
        ):
            assert (tmp_path / name).exists(), name
        assert json.loads((tmp_path / "registry.json").read_text())["repo"] == "dataset-incubator"

    def test_validation_error_blocks_write(
        self, tmp_path: Path, monkeypatch, _isolate_argv
    ) -> None:
        result = _result()
        result["errors"]["registry"]["validation"] = ["schema violato: x"]

        def fake(layout, *, derive_mode="local", **kwargs):
            return result

        monkeypatch.setattr("toolkit.registry.builders.build_registry", fake)
        sys.argv = ["build_registry.py", "--out", str(tmp_path), "--write"]
        code = br.main()
        assert code == 1
        assert not (tmp_path / "registry.json").exists()

    def test_derive_warning_is_not_blocking(
        self, tmp_path: Path, monkeypatch, _isolate_argv
    ) -> None:
        result = _result()
        result["errors"]["datasets"]["derive"] = ["demo_ds: nessun parquet locale"]

        def fake(layout, *, derive_mode="local", **kwargs):
            return result

        monkeypatch.setattr("toolkit.registry.builders.build_registry", fake)
        sys.argv = ["build_registry.py", "--out", str(tmp_path)]
        code = br.main()
        assert code == 0

    def test_existing_passed_to_builder(self, tmp_path: Path, patch_builder, _isolate_argv) -> None:
        (tmp_path / "clean_catalog.json").write_text(
            json.dumps({"datasets": [{"slug": "editoriale"}]}), encoding="utf-8"
        )
        sys.argv = ["build_registry.py", "--out", str(tmp_path)]
        br.main()
        kwargs = patch_builder["kwargs"]
        assert kwargs["existing_catalog"] == {"datasets": [{"slug": "editoriale"}]}
