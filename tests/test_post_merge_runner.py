"""
Test per post_merge_runner.py — contratto PR body + sample-run early exit.

Contratto:
  cmd_build_pr_body  genera il body markdown della PR registry da detect_output.json
  cmd_sample_run     processa config rilevati; con input vuoto deve uscire senza errori
  main()             CLI arg parsing

I test chiamano le funzioni direttamente (non via subprocess) per copertura reale.
"""

import argparse
import json
from pathlib import Path

import pytest

from scripts import post_merge_runner as pmr


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_detect_json(tmp_path: Path) -> Path:
    """Crea un detect_output.json con due config finti."""
    data = {
        "has_items": True,
        "has_configs": True,
        "items": [
            {"slug": "test-ds-1", "kind": "candidate", "root": "candidates/test-ds-1"},
            {"slug": "test-ds-2", "kind": "candidate", "root": "candidates/test-ds-2"},
        ],
        "configs": [
            {
                "kind": "candidate",
                "slug": "test-ds-1",
                "config_path": "candidates/test-ds-1/dataset.yml",
                "config_exists": True,
                "artifact_name": "test-ds-1",
                "is_nested": False,
                "push_slug": "test-ds-1",
            },
            {
                "kind": "candidate",
                "slug": "test-ds-2",
                "config_path": "candidates/test-ds-2/dataset.yml",
                "config_exists": True,
                "artifact_name": "test-ds-2",
                "is_nested": False,
                "push_slug": "test-ds-2",
            },
        ],
    }
    path = tmp_path / "detect_output.json"
    path.write_text(json.dumps(data))
    return path


@pytest.fixture
def empty_detect_json(tmp_path: Path) -> Path:
    """Crea un detect_output.json senza config ne items."""
    data = {
        "has_items": False,
        "has_configs": False,
        "items": [],
        "configs": [],
    }
    path = tmp_path / "detect_output_empty.json"
    path.write_text(json.dumps(data))
    return path


def _run_build_pr_body(detect_json: Path, tmp_path: Path, **overrides) -> str:
    """Helper: chiama cmd_build_pr_body e restituisce il body generato."""
    out = tmp_path / "body.md"
    kwargs = dict(
        detect_json=str(detect_json),
        pr_number="1",
        pr_title="test",
        sample_result="success",
        signals_changed="true",
        output=str(out),
    )
    kwargs.update(overrides)
    args = argparse.Namespace(**kwargs)
    pmr.cmd_build_pr_body(args)
    return out.read_text()


# ---------------------------------------------------------------------------
# build-pr-body
# ---------------------------------------------------------------------------


class TestBuildPrBody:
    @pytest.mark.pure_unit
    def test_generates_markdown(self, sample_detect_json: Path, tmp_path: Path):
        """build-pr-body produce markdown valido con i placeholder giusti."""
        body = _run_build_pr_body(
            sample_detect_json,
            tmp_path,
            pr_number="42",
            pr_title="feat: test dataset",
        )
        assert "## Post-merge registry handoff" in body
        assert "Source PR: #42" in body
        assert "feat: test dataset" in body
        assert "test-ds-1" in body
        assert "test-ds-2" in body
        assert "- [x] CI: full run completato" in body
        assert "Maintainer: push mart + BQ" in body
        assert "push_archive.py --mart --slug" in body
        # GCP env non settato in test → check vuoto
        assert "[ ] CI: clean parquet" in body

    @pytest.mark.pure_unit
    def test_no_diff_when_signals_unchanged(self, sample_detect_json: Path, tmp_path: Path):
        """(no diff) appare nel body quando signals_changed=false."""
        body = _run_build_pr_body(sample_detect_json, tmp_path, signals_changed="false")
        assert "(no diff)" in body

    @pytest.mark.pure_unit
    def test_sample_not_passed(self, sample_detect_json: Path, tmp_path: Path):
        """Check vuoto se sample fallisce."""
        body = _run_build_pr_body(sample_detect_json, tmp_path, sample_result="failure")
        assert "[ ] CI: full run" in body
        assert "[ ] CI: clean parquet" in body

    @pytest.mark.pure_unit
    def test_empty_items(self, empty_detect_json: Path, tmp_path: Path):
        """Con detect vuoto, il body segnala 'No sample-run config'."""
        body = _run_build_pr_body(empty_detect_json, tmp_path, sample_result="skipped")
        assert "No sample-run config detected" in body
        assert "push_archive.py" not in body

    @pytest.mark.pure_unit
    def test_gcp_available_shows_x(self, sample_detect_json: Path, tmp_path: Path, monkeypatch):
        """Con GCP env settati, i check GCS appaiono come [x]."""
        monkeypatch.setenv("GCP_WORKLOAD_IDENTITY_PROVIDER", "projects/p/...")
        monkeypatch.setenv("GCP_SERVICE_ACCOUNT", "sa@project.iam.gserviceaccount.com")
        body = _run_build_pr_body(sample_detect_json, tmp_path)
        assert "- [x] CI: clean parquet pushato su GCS" in body
        assert "- [x] CI: `registry/clean_catalog.json` aggiornato" in body


# ---------------------------------------------------------------------------
# sample-run — early exit
# ---------------------------------------------------------------------------


class TestSampleRun:
    @pytest.mark.smoke
    def test_empty_config_exits_cleanly(self, empty_detect_json: Path, capsys):
        """sample-run con detect vuoto deve uscire senza errori."""
        args = argparse.Namespace(
            detect_json=str(empty_detect_json),
            retry=3,
        )
        # Non deve sollevare SystemExit
        pmr.cmd_sample_run(args)
        captured = capsys.readouterr()
        assert "Nessun config da processare" in captured.out


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


class TestReadDetectJson:
    @pytest.mark.pure_unit
    def test_reads_valid_json(self, sample_detect_json: Path):
        result = pmr._read_detect_json(str(sample_detect_json))
        assert result["has_items"] is True
        assert len(result["configs"]) == 2

    @pytest.mark.pure_unit
    def test_file_not_found(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            pmr._read_detect_json(str(tmp_path / "nonexistent.json"))


# ---------------------------------------------------------------------------
# CLI arg parsing — via main() con sys.argv
# ---------------------------------------------------------------------------


class TestMain:
    @pytest.mark.pure_unit
    def test_no_command_shows_help(self):
        """Senza subcomando, SystemExit."""
        with pytest.raises(SystemExit):
            pmr.main()

    @pytest.mark.pure_unit
    def test_unknown_command_fails(self):
        """Subcomando sconosciuto, SystemExit."""
        with pytest.raises(SystemExit):
            with pytest.MonkeyPatch().context() as mp:
                mp.setattr("sys.argv", ["prog", "foobar"])
                pmr.main()

    @pytest.mark.pure_unit
    def test_build_pr_body_missing_required(self, tmp_path):
        """build-pr-body senza --pr-number fallisce."""
        detect = tmp_path / "detect.json"
        detect.write_text("{}")
        with pytest.raises(SystemExit):
            with pytest.MonkeyPatch().context() as mp:
                mp.setattr(
                    "sys.argv",
                    ["prog", "build-pr-body", "--detect-json", str(detect)],
                )
                pmr.main()

    @pytest.mark.pure_unit
    def test_build_pr_body_via_main(self, sample_detect_json, tmp_path):
        """build-pr-body via main() produce output."""
        out = tmp_path / "body.md"
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr(
                "sys.argv",
                [
                    "prog",
                    "build-pr-body",
                    "--detect-json",
                    str(sample_detect_json),
                    "--pr-number",
                    "99",
                    "--pr-title",
                    "via-main",
                    "--sample-result",
                    "success",
                    "--signals-changed",
                    "true",
                    "--output",
                    str(out),
                ],
            )
            pmr.main()
        body = out.read_text()
        assert "Source PR: #99" in body
        assert "via-main" in body

    @pytest.mark.pure_unit
    def test_sample_run_via_main_empty(self, empty_detect_json, capsys):
        """sample-run via main() con detect vuoto esce senza errori."""
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr(
                "sys.argv",
                ["prog", "sample-run", "--detect-json", str(empty_detect_json)],
            )
            pmr.main()
        captured = capsys.readouterr()
        assert "Nessun config da processare" in captured.out

    @pytest.mark.pure_unit
    def test_sample_run_skip_configs(self, tmp_path, capsys):
        """sample-run con config_exists=False deve skippare."""
        data = {
            "has_items": True,
            "has_configs": True,
            "items": [{"slug": "test", "kind": "candidate", "root": "candidates/test"}],
            "configs": [
                {
                    "kind": "candidate",
                    "slug": "test",
                    "config_path": "candidates/test/dataset.yml",
                    "config_exists": False,
                    "artifact_name": "test",
                    "is_nested": False,
                    "push_slug": "test",
                },
            ],
        }
        detect = tmp_path / "detect_skip.json"
        detect.write_text(json.dumps(data))
        args = argparse.Namespace(detect_json=str(detect), retry=3)
        pmr.cmd_sample_run(args)
        captured = capsys.readouterr()
        assert "SKIP: config_path non esiste" in captured.out

    @pytest.mark.pure_unit
    def test_run_with_retry_first_attempt_succeeds(self):
        """_run_with_retry ritorna True se il comando ha successo al primo tentativo."""
        result = pmr._run_with_retry(
            ["python", "-c", "exit(0)"],
            cwd=".",
            attempts=2,
        )
        assert result is True

    @pytest.mark.pure_unit
    def test_run_with_retry_second_attempt_succeeds(self):
        """_run_with_retry riprova se primo tentativo fallisce."""
        import subprocess

        # Fallisce 1 volta, poi succeede
        calls = [0]

        def _run_fail_once(*a, **kw):
            calls[0] += 1
            r = subprocess.CompletedProcess([], 1 if calls[0] == 1 else 0)
            return r

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(subprocess, "run", _run_fail_once)
        try:
            result = pmr._run_with_retry(["true"], cwd=".", attempts=2)
            assert result is True
        finally:
            monkeypatch.undo()
