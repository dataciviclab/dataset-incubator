"""
Test per detect_candidates.py — rilevamento candidate modificati da git diff.

Contratto: detect_candidates() produce items e configs per workflow CI.
  _detect_from_files() — parsifica file paths in items/configs
  _resolve_year() — legge anno da dataset.yml
  _dataset_name() — legge nome da dataset.yml

Prova del fuoco: se cancello questi test, un refactor di detect_candidates
puo' far rilevare candidate sbagliati ai workflow CI (pr-toolkit-check, post-merge).
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest


def _write_yml(path: Path, data: dict) -> None:
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


class TestResolveYear:
    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        "content,expected",
        [
            ({"dataset": {"years": [2020, 2021, 2022]}}, 2022),
            ({"dataset": {"years": []}}, 0),
            ({"dataset": {"years": "not-a-list"}}, 0),
        ],
    )
    def test(self, tmp_path, content, expected):
        from detect_candidates import _resolve_year

        cfg = tmp_path / "dataset.yml"
        _write_yml(cfg, content)
        assert _resolve_year(cfg) == expected

    @pytest.mark.contract
    def test_returns_zero_on_missing_file(self, tmp_path):
        from detect_candidates import _resolve_year

        assert _resolve_year(tmp_path / "nope.yml") == 0


class TestDatasetName:
    @pytest.mark.contract
    def test_returns_name(self, tmp_path):
        from detect_candidates import _dataset_name

        cfg = tmp_path / "dataset.yml"
        _write_yml(cfg, {"dataset": {"name": "Test DS"}})
        assert _dataset_name(cfg) == "Test DS"

    @pytest.mark.contract
    @pytest.mark.parametrize(
        "setup",
        [
            lambda cfg: None,  # file non esiste
            lambda cfg: cfg.write_text("{{invalid}}"),  # YAML non valido
        ],
    )
    def test_returns_none(self, tmp_path, setup):
        from detect_candidates import _dataset_name

        cfg = tmp_path / "dataset.yml"
        setup(cfg)
        assert _dataset_name(cfg) is None


class TestDetectFromFiles:
    @pytest.mark.contract
    @pytest.mark.parametrize(
        "files,expected_kinds",
        [
            (["candidates/ds/dataset.yml", "candidates/ds/sql/clean.sql"], ["candidate"]),
            (["support_datasets/sup/dataset.yml"], ["support_dataset"]),
            (["compose/agg/dataset.yml"], ["compose"]),
            (["candidates/a/a.yml", "candidates/a/b.yml"], ["candidate"]),  # unico item
        ],
    )
    def test_detects_kind(self, files, expected_kinds):
        from detect_candidates import _detect_from_files

        items, _ = _detect_from_files(files)
        assert len(items) == len(expected_kinds)
        for item, kind in zip(items, expected_kinds):
            assert item["kind"] == kind

    @pytest.mark.contract
    @pytest.mark.parametrize(
        "files",
        [
            ["README.md", ".gitignore"],
            ["scripts/build.py", ".github/workflows/ci.yml"],
        ],
    )
    def test_ignores_unrelated(self, files):
        from detect_candidates import _detect_from_files

        items, configs = _detect_from_files(files)
        assert items == []
        assert configs == []


class TestDetectCandidatesFiles:
    @pytest.mark.contract
    def test_files_mode_basic(self):
        from detect_candidates import detect_candidates

        result = detect_candidates(files=["candidates/my-ds/dataset.yml"])
        assert result["items"][0]["slug"] == "my-ds"

    @pytest.mark.contract
    def test_empty_files(self):
        from detect_candidates import detect_candidates

        assert detect_candidates(files=[])["has_items"] is False

    @pytest.mark.contract
    def test_config_exists(self, tmp_path):
        from detect_candidates import detect_candidates

        _write_yml(
            tmp_path / "candidates" / "root-ds" / "dataset.yml",
            {
                "dataset": {"name": "Root", "years": [2020]},
            },
        )
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with patch("detect_candidates.ROOT", tmp_path):
                result = detect_candidates(files=["candidates/root-ds/dataset.yml"])
        finally:
            os.chdir(old_cwd)
        assert result["configs"][0]["is_nested"] is False

    @pytest.mark.contract
    def test_config_nested(self, tmp_path):
        from detect_candidates import detect_candidates

        _write_yml(
            tmp_path / "candidates" / "multi" / "sources" / "fonte-a" / "dataset.yml",
            {
                "dataset": {"name": "FA", "years": [2020]},
            },
        )
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with patch("detect_candidates.ROOT", tmp_path):
                result = detect_candidates(files=["candidates/multi/sources/fonte-a/dataset.yml"])
        finally:
            os.chdir(old_cwd)
        assert result["configs"][0]["is_nested"] is True


class TestDetectCandidatesSlug:
    @pytest.mark.contract
    @pytest.mark.parametrize(
        "slug_dir,kind",
        [
            (("candidates", "my-ds"), "candidate"),
            (("compose", "agg"), "compose"),
            (("support_datasets", "sup"), "support_dataset"),
        ],
    )
    def test_finds_by_slug(self, tmp_path, slug_dir, kind):
        from detect_candidates import detect_candidates

        prefix, slug = slug_dir
        _write_yml(
            tmp_path / prefix / slug / "dataset.yml",
            {
                "dataset": {"name": slug, "years": [2020]},
            },
        )
        with patch("detect_candidates.ROOT", tmp_path):
            result = detect_candidates(slug=slug)
        assert result["items"][0]["kind"] == kind

    @pytest.mark.contract
    def test_not_found(self, tmp_path):
        from detect_candidates import detect_candidates

        with patch("detect_candidates.ROOT", tmp_path):
            assert detect_candidates(slug="nonexistent")["has_items"] is False

    @pytest.mark.contract
    def test_nested(self, tmp_path):
        from detect_candidates import detect_candidates

        _write_yml(
            tmp_path / "candidates" / "multi" / "sources" / "fonte-a" / "dataset.yml",
            {
                "dataset": {"name": "FA", "years": [2020]},
            },
        )
        with patch("detect_candidates.ROOT", tmp_path):
            assert detect_candidates(slug="multi")["configs"][0]["is_nested"] is True


class TestDetectCandidatesGit:
    @pytest.mark.contract
    def test_git_diff_mode(self):
        from detect_candidates import detect_candidates

        with patch("detect_candidates._git_diff_files") as mock_git:
            mock_git.return_value = ["candidates/test-ds/dataset.yml"]
            result = detect_candidates(base_sha="abc", head_sha="def")
        assert result["items"][0]["slug"] == "test-ds"


class TestGitDiffFiles:
    @pytest.mark.contract
    def test_returns_files(self):
        from detect_candidates import _git_diff_files

        with patch("detect_candidates.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "candidates/a/dataset.yml\ncandidates/b/sql/clean.sql\n"
            assert len(_git_diff_files("base", "head")) == 2

    @pytest.mark.contract
    def test_raises_on_error(self):
        from detect_candidates import _git_diff_files

        with patch("detect_candidates.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            import subprocess

            with pytest.raises(subprocess.CalledProcessError):
                _git_diff_files("base", "head")
