"""
Test per resolve_sample_run.py — risoluzione parametri sample run da dataset.yml.

Contratto: resolve() produce JSON con config_path, slug, sample_year, is_nested,
has_support, support. Usato dai workflow CI per determinare cosa eseguire.

Prova del fuoco: se cancello questi test, un refactor di resolve() puo'
fornire parametri errati ai workflow CI (anno sbagliato, slug rotto, support perso).
"""

from pathlib import Path

import pytest


def _write_yml(path: Path, data: dict) -> Path:
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
    return path


class TestResolve:
    SAMPLE_RUN = {
        "status": "passed",
        "run_id": "1",
        "run_url": "u",
        "checked_at": "2026-01-01",
        "year": 2023,
    }

    @pytest.mark.contract
    def test_happy_path(self, tmp_path):
        from resolve_sample_run import resolve

        ds = tmp_path / "candidates" / "test-ds"
        cfg = _write_yml(
            ds / "dataset.yml",
            {
                "dataset": {"name": "Test DS", "years": [2020, 2021, 2022]},
                "support": [{"name": "Base", "config": "../base/dataset.yml"}],
            },
        )
        _write_yml(ds / "../base/dataset.yml", {"dataset": {"name": "Base"}})
        result = resolve(str(cfg))
        assert result["slug"] == "test-ds"
        assert result["sample_year"] == 2022
        assert result["is_nested"] is False
        assert result["has_support"] is True

    @pytest.mark.contract
    def test_single_year(self, tmp_path):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / "candidates" / "single" / "dataset.yml",
            {
                "dataset": {"name": "Single", "years": [2023]},
            },
        )
        assert resolve(str(cfg))["sample_year"] == 2023

    @pytest.mark.policy
    def test_unsorted_years_takes_max(self, tmp_path):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / "candidates" / "unsorted" / "dataset.yml",
            {
                "dataset": {"name": "Unsorted", "years": [2022, 2020, 2021]},
            },
        )
        assert resolve(str(cfg))["sample_year"] == 2022

    @pytest.mark.contract
    @pytest.mark.parametrize(
        "content,error_pattern",
        [
            ("{invalid: yaml: : }", "Invalid YAML"),
            ("", "No 'dataset' section"),
        ],
    )
    def test_errors(self, tmp_path, content, error_pattern):
        from resolve_sample_run import resolve

        cfg = tmp_path / "bad.yml"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(content)
        result = resolve(str(cfg))
        assert "error" in result
        assert error_pattern in result["error"]

    @pytest.mark.contract
    def test_missing_years(self, tmp_path):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / "candidates" / "noyears" / "dataset.yml",
            {
                "dataset": {"name": "No Years"},
            },
        )
        assert "No 'dataset.years'" in resolve(str(cfg))["error"]

    @pytest.mark.contract
    def test_invalid_years_type(self, tmp_path):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / "candidates" / "badyears" / "dataset.yml",
            {
                "dataset": {"name": "Bad", "years": ["a", "b"]},
            },
        )
        assert "Invalid years" in resolve(str(cfg))["error"]

    @pytest.mark.contract
    @pytest.mark.parametrize(
        "support_key,config",
        [
            ("support", {"name": "Base", "config": "support/base.yml"}),
            ("dataset.support", {"name": "Base", "config": "support/base.yml"}),
        ],
    )
    def test_support_both_levels(self, tmp_path, support_key, config):
        from resolve_sample_run import resolve

        ds = tmp_path / "candidates" / "ds"
        yml = {"dataset": {"name": "DS", "years": [2020]}}
        if support_key == "support":
            yml["support"] = [config]
        else:
            yml["dataset"]["support"] = [config]
        _write_yml(ds / "dataset.yml", yml)
        _write_yml(ds / "support" / "base.yml", {"dataset": {"name": "Base"}})
        result = resolve(str(ds / "dataset.yml"))
        assert result["has_support"] is True

    @pytest.mark.contract
    def test_nested_config(self, tmp_path):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / "candidates" / "multi" / "sources" / "fonte-a" / "dataset.yml",
            {"dataset": {"name": "FA", "years": [2020]}},
        )
        result = resolve(str(cfg))
        assert result["is_nested"] is True

    @pytest.mark.contract
    @pytest.mark.parametrize("prefix", ["candidates", "support_datasets"])
    def test_slug_from_prefix(self, tmp_path, prefix):
        from resolve_sample_run import resolve

        cfg = _write_yml(
            tmp_path / prefix / "my-slug" / "dataset.yml",
            {
                "dataset": {"name": "My", "years": [2020]},
            },
        )
        assert resolve(str(cfg))["slug"] == "my-slug"

    @pytest.mark.contract
    def test_file_not_found(self, tmp_path):
        from resolve_sample_run import resolve

        assert "not found" in resolve(str(tmp_path / "nope.yml"))["error"].lower()
