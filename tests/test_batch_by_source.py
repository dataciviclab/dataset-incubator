"""Test per batch_by_source.py — orchestrazione preflight/run per fonte.

Contratto: scan_dataset_ymls() legge source_id dai dataset.yml (candidates,
support_datasets, compose); group_by_source() raggruppa per fonte;
evaluate_preflight() decide il successo di un report preflight.

Prova del fuoco: se il criterio di successo o il raggruppamento cambiano,
smoke-weekly e chi usa lo script rischiano di validare candidate con fonti
non raggiungibili o di escludere dataset dal batch.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import batch_by_source as bbs


def _write_yml(path: Path, content: dict) -> None:
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(content, f, default_flow_style=False)


class TestScan:
    @pytest.mark.pure_unit
    def test_legge_source_id_da_tutte_le_sezioni(self, tmp_path: Path) -> None:
        for section, name, sid in (
            ("candidates", "openga-a", "openga"),
            ("support_datasets", "support-x", "istat"),
            ("compose", "compose-y", "dataciviclab_composite"),
        ):
            _write_yml(
                tmp_path / section / name / "dataset.yml",
                {"dataset": {"name": name, "years": [2024], "source_id": sid}},
            )

        entries = bbs.scan_dataset_ymls(tmp_path)
        assert len(entries) == 3
        assert {e.source_id for e in entries} == {"openga", "istat", "dataciviclab_composite"}

    @pytest.mark.pure_unit
    def test_senza_source_id_viene_marcato_unknown(self, tmp_path: Path) -> None:
        _write_yml(
            tmp_path / "candidates" / "no-src" / "dataset.yml",
            {"dataset": {"name": "no_src", "years": [2024]}},
        )
        entries = bbs.scan_dataset_ymls(tmp_path)
        assert len(entries) == 1
        assert entries[0].source_id == bbs.UNKNOWN_SOURCE

    @pytest.mark.pure_unit
    def test_ignora_directory_senza_dataset_yml(self, tmp_path: Path) -> None:
        (tmp_path / "candidates" / "vuoto").mkdir(parents=True)
        assert bbs.scan_dataset_ymls(tmp_path) == []


class TestGroup:
    @pytest.mark.pure_unit
    def test_raggruppa_e_ordina_per_fonte(self, tmp_path: Path) -> None:
        for name, sid in (("b-ds", "zeta"), ("a-ds", "alfa"), ("c-ds", "alfa")):
            _write_yml(
                tmp_path / "candidates" / name / "dataset.yml",
                {"dataset": {"name": name, "years": [2024], "source_id": sid}},
            )
        groups = bbs.group_by_source(bbs.scan_dataset_ymls(tmp_path))
        assert list(groups.keys()) == ["alfa", "zeta"]
        assert [e.path.parent.name for e in groups["alfa"]] == ["a-ds", "c-ds"]


class TestEvaluate:
    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        "result,expected_ok,expected_str",
        [
            # tutte le fonti raggiungibili
            (
                {"status": "passed", "sources": [{"reachable": True}, {"reachable": True}]},
                True,
                "2/2",
            ),
            # una fonte non raggiungibile
            (
                {"status": "passed", "sources": [{"reachable": True}, {"reachable": False}]},
                False,
                "1/2",
            ),
            # nessuna fonte (local_file) → ok, non fallisce per conteggio
            ({"status": "passed", "sources": []}, True, "-"),
            # status failed
            ({"status": "failed", "sources": []}, False, "-"),
            # fonti skipped escluse dal denominatore
            (
                {
                    "status": "passed",
                    "sources": [
                        {"reachable": True},
                        {"reachable": False, "status": "skipped"},
                    ],
                },
                True,
                "1/1",
            ),
        ],
    )
    def test_criterio_successo(self, result, expected_ok, expected_str) -> None:
        ok, reachable = bbs.evaluate_preflight(result)
        assert ok is expected_ok
        assert reachable == expected_str


class TestSmoke:
    @pytest.mark.smoke
    @pytest.mark.skipif(shutil.which("toolkit") is None, reason="toolkit non installato nel PATH")
    def test_preflight_reale_su_local_file(self, tmp_path: Path) -> None:
        """Preflight reale su un candidate local_file (zero rete)."""
        ds = tmp_path / "candidates" / "smoke-ds"
        ds.mkdir(parents=True)
        raw = ds / "raw_data"
        raw.mkdir()
        (raw / "data_2024.csv").write_text("anno;valore\n2024;100\n", encoding="utf-8")
        _write_yml(
            ds / "dataset.yml",
            {
                "dataset": {"name": "smoke_ds", "years": [2024], "source_id": "smoke"},
                "raw": {
                    "sources": [
                        {
                            "name": "fonte",
                            "type": "local_file",
                            "args": {"path": str(raw / "data_2024.csv")},
                        }
                    ]
                },
            },
        )

        result = bbs.run_preflight(ds / "dataset.yml", timeout=30)
        # Il JSON del preflight è sempre parsato (anche su failed)
        assert "status" in result
        ok, reachable = bbs.evaluate_preflight(result)
        # local_file → fonte probe come "skipped": nessuna fonte attiva → ok con "-"
        assert ok is True
        assert reachable == "-"
