# ruff: noqa: E402
"""Test per scripts/build_registry.py — wrapper fusion del registry.

Contratto: il wrapper produce registry.json unico (fusion ADR). La logica di
derivazione è del toolkit; qui si testa il layout DI (existing preservato dal
registry.json, exit codes).

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
    def test_no_registry_returns_none(self, tmp_path: Path) -> None:
        catalog, signals = br._load_existing(tmp_path)
        assert catalog is None
        assert signals is None

    def test_registry_json_loaded(self, tmp_path: Path) -> None:
        (tmp_path / "registry.json").write_text(
            json.dumps(
                {
                    "datasets": [{"slug": "a"}],
                    "marts": [{"slug": "a__m"}],
                    "signals": [{"id": "a"}],
                }
            ),
            encoding="utf-8",
        )
        catalog, signals = br._load_existing(tmp_path)
        assert catalog == {"datasets": [{"slug": "a"}], "marts": [{"slug": "a__m"}]}
        assert signals == {"signals": [{"id": "a"}]}

    def test_registry_corrupt_returns_none(self, tmp_path: Path) -> None:
        (tmp_path / "registry.json").write_text("{not json", encoding="utf-8")
        catalog, signals = br._load_existing(tmp_path)
        assert catalog is None
        assert signals is None


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

    def test_write_produces_only_registry(
        self, tmp_path: Path, patch_builder, _isolate_argv
    ) -> None:
        sys.argv = ["build_registry.py", "--out", str(tmp_path), "--write"]
        code = br.main()
        assert code == 0
        assert (tmp_path / "registry.json").exists()
        # Niente più proiezioni legacy
        assert not (tmp_path / "clean_catalog.json").exists()
        assert not (tmp_path / "pipeline_signals.json").exists()
        assert not (tmp_path / "entity_graph.json").exists()
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
        (tmp_path / "registry.json").write_text(
            json.dumps({"datasets": [{"slug": "editoriale"}], "marts": []}),
            encoding="utf-8",
        )
        sys.argv = ["build_registry.py", "--out", str(tmp_path)]
        br.main()
        kwargs = patch_builder["kwargs"]
        assert kwargs["existing_catalog"] == {
            "datasets": [{"slug": "editoriale"}],
            "marts": [],
        }
