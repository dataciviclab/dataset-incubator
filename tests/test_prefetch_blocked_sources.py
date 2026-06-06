"""Test per scripts/prefetch_blocked_sources.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.prefetch_blocked_sources import (
    BLOCKED_PATTERNS,
    _is_blocked,
    _patch_config,
)

pytestmark = pytest.mark.pure_unit


class TestIsBlocked:
    """Test pattern matching per fonti bloccate."""

    def test_blocked_salute(self):
        assert _is_blocked("https://www.dati.salute.gov.it/dataset/file.csv")

    def test_blocked_salute_no_www(self):
        assert _is_blocked("http://dati.salute.gov.it/dataset/file.csv")

    def test_not_blocked_istat(self):
        assert not _is_blocked("https://www.istat.it/data.zip")

    def test_not_blocked_github(self):
        assert not _is_blocked("https://raw.githubusercontent.com/data.csv")


class TestPatchConfig:
    """Test trasformazione dataset.yml."""

    BLOCKED_URL = "https://dati.salute.gov.it/file.csv"

    def test_http_to_local_file(self, tmp_path: Path):
        cfg = tmp_path / "dataset.yml"
        cfg.write_text(
            "raw:\n"
            "  sources:\n"
            "    - name: test\n"
            "      type: http_file\n"
            "      args:\n"
            "        url: https://dati.salute.gov.it/file.csv\n"
        )
        _patch_config(cfg, Path("data/raw/test/2022/file.csv"), blocked_url=self.BLOCKED_URL)

        content = cfg.read_text()
        assert "type: local_file" in content
        assert "data/raw/test/2022/file.csv" in content
        assert "dati.salute.gov.it" not in content

    def test_only_blocked_source_changed(self, tmp_path: Path):
        """Solo la source con URL bloccato viene modificata."""
        cfg = tmp_path / "dataset.yml"
        cfg.write_text(
            "raw:\n"
            "  sources:\n"
            "    - name: salute\n"
            "      type: http_file\n"
            "      args:\n"
            "        url: https://dati.salute.gov.it/bloccato.csv\n"
            "    - name: istat\n"
            "      type: http_file\n"
            "      args:\n"
            "        url: https://www.istat.it/data.zip\n"
        )
        _patch_config(
            cfg,
            Path("data/raw/salute/bloccato.csv"),
            blocked_url="https://dati.salute.gov.it/bloccato.csv",
        )

        content = cfg.read_text()
        # Quella bloccata: local_file, niente url
        assert "type: local_file" in content
        assert "dati.salute.gov.it" not in content
        # Quella non bloccata: ancora http_file con url
        assert "www.istat.it" in content
        # Verifica esplicita: il type della seconda source è ancora http_file
        # (yaml.dump produce type: http_file senza virgolette)
        assert "type: http_file" in content

    def test_no_blocked_url_does_nothing(self, tmp_path: Path):
        """Se blocked_url non matcha nessuna source, il file non cambia."""
        cfg = tmp_path / "dataset.yml"
        cfg.write_text("raw:\n  sources:\n    - name: a\n      type: local_file\n")
        before = cfg.read_text()
        _patch_config(cfg, Path("x.csv"), blocked_url="https://altro.it/x.csv")
        assert cfg.read_text() == before


class TestPatternsList:
    """I pattern non devono essere vuoti e devono funzionare."""

    def test_patterns_are_compiled(self):
        for p in BLOCKED_PATTERNS:
            assert p.search("https://www.dati.salute.gov.it/test.csv")

    def test_patterns_reject_other(self):
        for p in BLOCKED_PATTERNS:
            assert not p.search("https://www.istat.it/data.csv")
