"""Test per scripts/prefetch_blocked_sources.py."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from scripts.prefetch_blocked_sources import (
    BLOCKED_PATTERNS,
    _is_blocked,
    _patch_config,
)


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

    def test_http_to_local_file(self, tmp_path: Path):
        cfg = tmp_path / "dataset.yml"
        cfg.write_text(
            "root: '../../out'\n"
            "raw:\n"
            "  sources:\n"
            "    - name: test\n"
            "      type: 'http_file'\n"
            "      args:\n"
            "        url: 'https://dati.salute.gov.it/file.csv'\n"
            "        filename: 'file.csv'\n"
            "      primary: true\n"
        )
        raw_path = Path("out/data/raw/test/2022/file.csv")
        _patch_config(cfg, raw_path)

        content = cfg.read_text()
        assert "type: 'local_file'" in content
        assert "path: out/data/raw/test/2022/file.csv" in content
        assert "url: 'https://dati.salute.gov.it/file.csv'" not in content

    def test_url_removed(self, tmp_path: Path):
        """La vecchia url deve sparire."""
        cfg = tmp_path / "dataset.yml"
        cfg.write_text("url: 'https://dati.salute.gov.it/x.csv'\n")
        _patch_config(cfg, Path("new_path.csv"))
        assert "https://dati.salute.gov.it" not in cfg.read_text()


class TestPatternsList:
    """I pattern non devono essere vuoti e devono funzionare."""

    def test_patterns_are_compiled(self):
        for p in BLOCKED_PATTERNS:
            assert p.search("https://www.dati.salute.gov.it/test.csv")

    def test_patterns_reject_other(self):
        for p in BLOCKED_PATTERNS:
            assert not p.search("https://www.istat.it/data.csv")
