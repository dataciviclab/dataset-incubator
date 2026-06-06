"""
Test per build_pipeline_signals.py — contratto pipeline_signals.json per ACB.

Contratto: build_signals() produce un file JSON con schema validato
che agent-context-builder consuma come segnale di stato pipeline.
  _inspect_*    — ispeziona directory candidate e produce dict strutturato
  _build_signal — combina layout + ispezione in un entry per signals[]
  load_previous_sample_runs — legge stato precedente dal JSON esistente

Prova del fuoco: se cancello questi test, un refactor di build_pipeline_signals
può rompere il formato pipeline_signals.json che ACB si aspetta.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest


def _write_yaml(path, data):
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def _single_source(base: Path, name="ds", years=None, sources=None, mart=True):
    d = base / name
    (d / "sql").mkdir(parents=True)
    (d / "sql" / "clean.sql").write_text("SELECT 1")
    if mart:
        (d / "sql" / "mart.sql").write_text("SELECT * FROM clean")
    _write_yaml(
        d / "dataset.yml",
        {
            "dataset": {"name": name, "years": years or [2020]},
            "raw": {"sources": sources or [{"name": "Fonte"}]},
        },
    )
    return d


class TestYearsLabel:
    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        "years,expected",
        [
            ([2023], "anno 2023"),
            ([2020, 2021, 2022], "anni 2020-2022"),
            ([], "anni: ?"),
            ([2022, 2020, 2021], "anni 2020-2022"),
        ],
    )
    def test(self, years, expected):
        from build_pipeline_signals import _years_label

        assert _years_label(years) == expected


class TestSourceNames:
    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        "sources,expected",
        [
            ([{"name": "A"}, {"name": "B"}], ["A", "B"]),
            ([{"name": "OK"}, "string", 42], ["OK"]),
            ([{"url": "http://x"}], ["?"]),
            ([], []),
        ],
    )
    def test(self, sources, expected):
        from build_pipeline_signals import _source_names

        assert _source_names(sources) == expected


class TestInspectSingleSource:
    @pytest.mark.contract
    def test_ok(self, tmp_path):
        from build_pipeline_signals import _inspect_single_source

        base = _single_source(tmp_path, "ok")
        result = _inspect_single_source(base)
        assert result["pattern"] == "single-source"
        assert result["mart_ok"] is True
        assert result["failures"] == []

    @pytest.mark.contract
    def test_missing_dataset_yml(self, tmp_path):
        from build_pipeline_signals import _inspect_single_source

        base = tmp_path / "missing-yml"
        (base / "sql").mkdir(parents=True)
        (base / "sql" / "clean.sql").write_text("SELECT 1")
        result = _inspect_single_source(base)
        assert "missing dataset.yml" in result["failures"]

    @pytest.mark.contract
    def test_missing_sql_dir(self, tmp_path):
        from build_pipeline_signals import _inspect_single_source

        base = tmp_path / "missing-sql"
        base.mkdir(parents=True)
        _write_yaml(base / "dataset.yml", {"dataset": {"name": "x"}})
        result = _inspect_single_source(base)
        assert "missing sql/" in result["failures"]

    @pytest.mark.contract
    def test_missing_clean_sql(self, tmp_path):
        from build_pipeline_signals import _inspect_single_source

        base = tmp_path / "missing-clean"
        (base / "sql").mkdir(parents=True)
        _write_yaml(base / "dataset.yml", {"dataset": {"name": "x"}})
        result = _inspect_single_source(base)
        assert "missing sql/clean.sql" in result["failures"]

    @pytest.mark.policy
    def test_no_mart_is_not_failure(self, tmp_path):
        """Senza mart → warn, non failure."""
        from build_pipeline_signals import _inspect_single_source

        base = _single_source(tmp_path, "no-mart", mart=False)
        result = _inspect_single_source(base)
        assert result["mart_ok"] is False
        assert result["failures"] == []


class TestInspectMultiSource:
    @pytest.mark.contract
    def test_two_sources(self, tmp_path):
        from build_pipeline_signals import _inspect_multi_source

        base = tmp_path / "multi"
        _single_source(base / "sources", "a", years=[2020])
        _single_source(base / "sources", "b", years=[2021], sources=[{"name": "F B"}])
        result = _inspect_multi_source(base)
        assert result["pattern"] == "multi-source"
        assert sorted(result["years"]) == [2020, 2021]

    @pytest.mark.contract
    def test_compose_layer_makes_mart_ok(self, tmp_path):
        from build_pipeline_signals import _inspect_multi_source

        base = tmp_path / "multi-compose"
        _single_source(base / "sources", "a", years=[2020], mart=False)
        (base / "compose" / "sql").mkdir(parents=True)
        (base / "compose" / "sql" / "mart.sql").write_text("SELECT *")
        result = _inspect_multi_source(base)
        assert result["mart_ok"] is True

    @pytest.mark.policy
    def test_compose_without_mart_reports_warning(self, tmp_path):
        from build_pipeline_signals import _inspect_multi_source

        base = tmp_path / "multi-compose-nomart"
        _single_source(base / "sources", "a", years=[2020], mart=False)
        (base / "compose" / "sql").mkdir(parents=True)
        result = _inspect_multi_source(base)
        assert "present but missing mart SQL" in " ".join(result["failures"])


class TestInspectCompose:
    @pytest.mark.contract
    def test_ok(self, tmp_path):
        from build_pipeline_signals import _inspect_compose

        base = tmp_path / "compose-ok"
        (base / "sql").mkdir(parents=True)
        (base / "sql" / "mart.sql").write_text("SELECT *")
        _write_yaml(
            base / "dataset.yml",
            {
                "dataset": {"name": "C", "years": [2020]},
                "support": [{"name": "Base"}],
            },
        )
        result = _inspect_compose(base)
        assert result["pattern"] == "compose"
        assert result["mart_ok"] is True
        assert result["failures"] == []

    @pytest.mark.contract
    def test_missing_mart(self, tmp_path):
        from build_pipeline_signals import _inspect_compose

        base = tmp_path / "compose-nomart"
        (base / "sql").mkdir(parents=True)
        _write_yaml(base / "dataset.yml", {"dataset": {"name": "C"}})
        result = _inspect_compose(base)
        assert result["mart_ok"] is False
        assert any("mart" in f for f in result["failures"])

    @pytest.mark.contract
    def test_missing_yml(self, tmp_path):
        from build_pipeline_signals import _inspect_compose

        base = tmp_path / "compose-noyml"
        (base / "sql").mkdir(parents=True)
        (base / "sql" / "mart.sql").write_text("SELECT *")
        result = _inspect_compose(base)
        assert "missing dataset.yml" in result["failures"]


class TestLoadPreviousSampleRuns:
    _SAMPLE_RUN = {
        "status": "passed",
        "run_id": "1",
        "run_url": "u",
        "checked_at": "2026-01-01",
        "year": 2023,
    }

    @pytest.mark.contract
    def test_loads(self, tmp_path):
        from build_pipeline_signals import load_previous_sample_runs

        p = tmp_path / "sig.json"
        p.write_text(
            json.dumps(
                {
                    "signals": [
                        {"id": "ds1", "sample_run": self._SAMPLE_RUN},
                        {"id": "ds2", "sample_run": {**self._SAMPLE_RUN, "year": 2024}},
                    ]
                }
            )
        )
        r = load_previous_sample_runs(p)
        assert "ds1" in r and "ds2" in r

    @pytest.mark.policy
    def test_skips_without_sample_run(self, tmp_path):
        from build_pipeline_signals import load_previous_sample_runs

        p = tmp_path / "sig.json"
        p.write_text(
            json.dumps(
                {
                    "signals": [
                        {"id": "ds1", "sample_run": self._SAMPLE_RUN},
                        {"id": "ds2"},
                    ]
                }
            )
        )
        r = load_previous_sample_runs(p)
        assert "ds1" in r and "ds2" not in r

    @pytest.mark.contract
    def test_skips_non_dict(self, tmp_path):
        from build_pipeline_signals import load_previous_sample_runs

        p = tmp_path / "sig.json"
        p.write_text(json.dumps({"signals": ["s", 42]}))
        assert load_previous_sample_runs(p) == {}

    @pytest.mark.contract
    def test_missing_file(self, tmp_path):
        from build_pipeline_signals import load_previous_sample_runs

        assert load_previous_sample_runs(tmp_path / "nope.json") == {}

    @pytest.mark.contract
    def test_invalid_json(self, tmp_path):
        from build_pipeline_signals import load_previous_sample_runs

        (tmp_path / "bad.json").write_text("not json")
        assert load_previous_sample_runs(tmp_path / "bad.json") == {}


class TestBuildSignal:
    @pytest.mark.contract
    def test_single_source_ok(self, tmp_path):
        from build_pipeline_signals import _build_signal

        base = _single_source(tmp_path, "ok-ds", years=[2020], sources=[{"name": "F", "url": "u"}])
        _write_yaml(
            base / "dataset.yml",
            {
                "dataset": {"name": "OK", "years": [2020], "source_id": "src-1"},
                "raw": {"sources": [{"name": "F", "url": "u"}]},
            },
        )
        s = _build_signal("ok-ds", base)
        assert s["id"] == "ok-ds"
        assert s["source_id"] == "src-1"
        assert s["status"] == "ok"

    @pytest.mark.contract
    def test_warn_no_mart(self, tmp_path):
        from build_pipeline_signals import _build_signal

        base = _single_source(tmp_path, "warn-ds", mart=False)
        s = _build_signal("warn-ds", base)
        assert s["status"] == "warn"

    @pytest.mark.contract
    def test_ambiguous_layout(self, tmp_path):
        from build_pipeline_signals import _build_signal

        base = tmp_path / "ambig"
        (base / "sql").mkdir(parents=True)
        (base / "sql" / "clean.sql").write_text("SELECT 1")
        (base / "sources").mkdir()
        _write_yaml(base / "dataset.yml", {"dataset": {"name": "Amb"}})
        s = _build_signal("ambig", base)
        assert s["status"] == "error"


class TestBuildSignals:
    @pytest.mark.contract
    def test_builds_from_candidates(self, tmp_path):
        from build_pipeline_signals import build_signals

        root = tmp_path / "repo"
        reg = root / "registry"
        _single_source(root / "candidates", "ok-ds")
        _single_source(root / "candidates", "warn-ds", mart=False)
        out = reg / "pipeline_signals.json"
        with patch("build_pipeline_signals.ROOT", root):
            assert build_signals(out) == 0
        payload = json.loads(out.read_text())
        assert payload["schema_version"] == "1"
        assert len(payload["signals"]) == 2

    @pytest.mark.contract
    def test_includes_support_and_compose(self, tmp_path):
        from build_pipeline_signals import build_signals

        root = tmp_path / "repo-full"
        reg = root / "registry"
        _single_source(root / "candidates", "ds")
        _single_source(root / "support_datasets", "sup", mart=False)
        comp = root / "compose" / "agg"
        (comp / "sql").mkdir(parents=True)
        (comp / "sql" / "mart.sql").write_text("SELECT *")
        _write_yaml(
            comp / "dataset.yml",
            {
                "dataset": {"name": "Agg", "years": [2020]},
                "support": [{"name": "Base"}],
            },
        )
        out = reg / "pipeline_signals.json"
        with patch("build_pipeline_signals.ROOT", root):
            assert build_signals(out) == 0
        ids = [s["id"] for s in json.loads(out.read_text())["signals"]]
        assert all(x in ids for x in ["ds", "sup", "compose:agg"])

    @pytest.mark.contract
    def test_preserves_sample_runs(self, tmp_path):
        from build_pipeline_signals import build_signals

        root = tmp_path / "repo-sample"
        reg = root / "registry"
        reg.mkdir(parents=True)
        (reg / "pipeline_signals.json").write_text(
            json.dumps(
                {
                    "signals": [
                        {
                            "id": "ok-ds",
                            "sample_run": {
                                "status": "passed",
                                "run_id": "r1",
                                "run_url": "u",
                                "checked_at": "2026-01-01",
                                "year": 2023,
                            },
                        }
                    ],
                }
            )
        )
        _single_source(root / "candidates", "ok-ds")
        out = reg / "pipeline_signals.json"
        with patch("build_pipeline_signals.ROOT", root):
            assert build_signals(out) == 0
        s = json.loads(out.read_text())["signals"][0]
        assert s["sample_run"]["run_id"] == "r1"

    @pytest.mark.contract
    def test_handles_no_candidates_dir(self, tmp_path):
        from build_pipeline_signals import build_signals

        root = tmp_path / "empty"
        out = root / "registry" / "pipeline_signals.json"
        with patch("build_pipeline_signals.ROOT", root):
            assert build_signals(out) == 1
        assert not out.exists()

    @pytest.mark.contract
    def test_handles_empty_candidates(self, tmp_path):
        from build_pipeline_signals import build_signals

        root = tmp_path / "empty-ok"
        (root / "candidates").mkdir(parents=True)
        out = root / "registry" / "pipeline_signals.json"
        with patch("build_pipeline_signals.ROOT", root):
            assert build_signals(out) == 0
        assert json.loads(out.read_text())["summary"]["total"] == 0
