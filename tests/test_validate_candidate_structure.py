"""
Test per validate_candidate_structure.py — validazione struttura candidate.

Contratto: validate_entry() controlla la struttura di directory dei candidate
e registra failure. Usato in CI e come building block per pipeline_signals.

Prova del fuoco: se cancello questi test, una modifica alla logica di validazione
puo' far passare candidate con struttura errata senza preavviso.
"""
from pathlib import Path

import pytest


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")


def _mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


class TestDetectCandidateLayout:
    @pytest.mark.contract
    @pytest.mark.parametrize("setup,expected", [
        (lambda b: _touch(b / "dataset.yml"), "single-source"),
        (lambda b: _mkdir(b / "sources" / "a"), "multi-source"),
        (lambda b: None, "unknown"),
    ])
    def test(self, tmp_path, setup, expected):
        from validate_candidate_structure import detect_candidate_layout
        base = tmp_path / "candidates" / "ds"
        setup(base)
        assert detect_candidate_layout(base)["layout"] == expected

    @pytest.mark.contract
    def test_ambiguous(self, tmp_path):
        from validate_candidate_structure import detect_candidate_layout
        base = tmp_path / "candidates" / "ds"
        _touch(base / "dataset.yml")
        _mkdir(base / "sources" / "a")
        assert detect_candidate_layout(base)["layout"] == "ambiguous"

    @pytest.mark.contract
    @pytest.mark.parametrize("prefix", ["support_datasets", "compose"])
    def test_special_dirs(self, tmp_path, prefix):
        from validate_candidate_structure import detect_candidate_layout
        base = tmp_path / prefix / "ds"
        _touch(base / "dataset.yml")
        expected = "support-dataset" if prefix == "support_datasets" else "compose"
        assert detect_candidate_layout(base)["layout"] == expected


class TestHasMartSql:
    @pytest.mark.contract
    @pytest.mark.parametrize("setup,expected", [
        (lambda s: (_mkdir(s), _touch(s / "mart.sql")), True),
        (lambda s: (_mkdir(s / "mart"), _touch(s / "mart" / "query.sql")), True),
        (lambda s: (_mkdir(s), _touch(s / "clean.sql")), False),
        (lambda s: _mkdir(s), False),
    ])
    def test(self, tmp_path, setup, expected):
        from validate_candidate_structure import has_mart_sql
        sql = tmp_path / "sql"
        setup(sql)
        assert has_mart_sql(sql) is expected


class TestValidateRootDocs:
    @pytest.mark.contract
    def test_reports_missing(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_root_docs
        base = patch_root / "ds"
        _mkdir(base)
        failures: list[str] = []
        validate_root_docs(base, failures)
        assert len(failures) == 2

    @pytest.mark.contract
    def test_ok_when_both_exist(self, tmp_path):
        from validate_candidate_structure import validate_root_docs
        base = tmp_path / "ds"
        _touch(base / "README.md")
        _touch(base / "notes.md")
        failures: list[str] = []
        validate_root_docs(base, failures)
        assert failures == []


class TestValidateSingleSource:
    @pytest.mark.contract
    def test_ok(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_single_source
        base = patch_root / "ds"
        _touch(base / "dataset.yml")
        _mkdir(base / "sql")
        _touch(base / "sql" / "clean.sql")
        _touch(base / "sql" / "mart.sql")
        failures: list[str] = []
        validate_single_source(base, failures)
        assert failures == []

    @pytest.mark.contract
    @pytest.mark.parametrize("setup,expect", [
        (lambda b: (_mkdir(b / "sql"), _touch(b / "sql" / "clean.sql")),
         "dataset.yml"),
        (lambda b: _touch(b / "dataset.yml"), "sql"),
        (lambda b: (_touch(b / "dataset.yml"), _mkdir(b / "sql")),
         "clean.sql"),
        (lambda b: (_touch(b / "dataset.yml"), _mkdir(b / "sql"),
                     _touch(b / "sql" / "clean.sql")),
         "mart"),
    ])
    def test_missing(self, tmp_path, patch_root, setup, expect):
        from validate_candidate_structure import validate_single_source
        base = patch_root / "ds"
        setup(base)
        failures: list[str] = []
        validate_single_source(base, failures)
        assert any(expect in f for f in failures)


class TestValidateComposeRoot:
    @pytest.mark.contract
    def test_ok(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_compose_root
        base = patch_root / "compose" / "ds"
        _touch(base / "dataset.yml")
        _mkdir(base / "sql")
        _touch(base / "sql" / "mart.sql")
        failures: list[str] = []
        validate_compose_root(base, failures)
        assert failures == []

    @pytest.mark.contract
    def test_missing_mart(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_compose_root
        base = patch_root / "compose" / "ds"
        _touch(base / "dataset.yml")
        _mkdir(base / "sql")
        failures: list[str] = []
        validate_compose_root(base, failures)
        assert any("mart" in f for f in failures)


class TestValidateMultiSource:
    @pytest.mark.contract
    def test_ok(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_multi_source
        base = patch_root / "candidates" / "multi"
        _touch(base / "sources" / "a" / "dataset.yml")
        _touch(base / "sources" / "a" / "sql" / "clean.sql")
        _touch(base / "sources" / "a" / "sql" / "mart.sql")
        failures: list[str] = []
        validate_multi_source(base, failures)
        assert failures == []

    @pytest.mark.contract
    def test_no_sources(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_multi_source
        base = patch_root / "candidates" / "multi"
        _mkdir(base / "sources")
        failures: list[str] = []
        validate_multi_source(base, failures)
        assert any("source directories" in f for f in failures)

    @pytest.mark.contract
    def test_missing_source_yml(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_multi_source
        base = patch_root / "candidates" / "multi"
        _mkdir(base / "sources" / "a")
        failures: list[str] = []
        validate_multi_source(base, failures)
        assert any("dataset.yml" in f for f in failures)

    @pytest.mark.policy
    def test_validate_compose_called(self, tmp_path, patch_root):
        """validate_multi_source chiama validate_compose per il compose layer."""
        from validate_candidate_structure import validate_multi_source
        base = patch_root / "candidates" / "multi"
        _touch(base / "sources" / "a" / "dataset.yml")
        _touch(base / "sources" / "a" / "sql" / "clean.sql")
        _touch(base / "sources" / "a" / "sql" / "mart.sql")
        _mkdir(base / "compose" / "sql")
        failures: list[str] = []
        validate_multi_source(base, failures)
        assert any("compose" in f for f in failures)


class TestValidateEntry:
    @pytest.mark.contract
    def test_single_source_ok(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_entry
        base = patch_root / "candidates" / "ds"
        _touch(base / "dataset.yml")
        _touch(base / "README.md")
        _touch(base / "notes.md")
        _mkdir(base / "sql")
        _touch(base / "sql" / "clean.sql")
        _touch(base / "sql" / "mart.sql")
        failures: list[str] = []
        validate_entry(base, failures)
        assert failures == []

    @pytest.mark.contract
    def test_missing_docs(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_entry
        base = patch_root / "candidates" / "ds"
        _touch(base / "dataset.yml")
        _mkdir(base / "sql")
        _touch(base / "sql" / "clean.sql")
        _touch(base / "sql" / "mart.sql")
        failures: list[str] = []
        validate_entry(base, failures)
        assert any("README.md" in f for f in failures)

    @pytest.mark.contract
    def test_ambiguous(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_entry
        base = patch_root / "candidates" / "ambig"
        _touch(base / "dataset.yml")
        _mkdir(base / "sources" / "a")
        failures: list[str] = []
        validate_entry(base, failures)
        assert any("ambiguous" in f for f in failures)

    @pytest.mark.contract
    def test_unknown(self, tmp_path, patch_root):
        from validate_candidate_structure import validate_entry
        base = patch_root / "candidates" / "empty"
        base.mkdir(parents=True)
        failures: list[str] = []
        validate_entry(base, failures)
        assert any("no valid structure" in f for f in failures)
