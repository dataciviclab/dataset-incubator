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
        # Dopo yaml.dump: type: local_file (senza virgolette)
        assert "type: local_file" in content
        # path presente e url assente
        assert str(raw_path) in content
        assert "dati.salute.gov.it" not in content

    def test_url_removed_when_no_sources(self, tmp_path: Path):
        """Se non ci sono raw.sources, il file non viene modificato."""
        cfg = tmp_path / "dataset.yml"
        cfg.write_text("key: value\n")
        before = cfg.read_text()
        _patch_config(cfg, Path("new_path.csv"))
        after = cfg.read_text()
        # yaml.dump può cambiare la formattazione, ma il contenuto deve
        # rimanere sostanzialmente lo stesso (nessuna trasformazione)
        assert "key: value" in after

    def test_multiple_sources_only_blocked_changed(self, tmp_path: Path):
        """Solo i source con type=http_file e url bloccato vengono modificati."""
        cfg = tmp_path / "dataset.yml"
        cfg.write_text(
            "raw:\n"
            "  sources:\n"
            "    - name: a\n"
            "      type: http_file\n"
            "      args:\n"
            "        url: https://dati.salute.gov.it/a.csv\n"
            "    - name: b\n"
            "      type: local_file\n"
            "      args:\n"
            "        path: data.csv\n"
        )
        _patch_config(cfg, Path("data/raw/a/2022/a.csv"))
        content = cfg.read_text()
        assert "type: local_file" in content or "type: 'local_file'" in content
        assert "dati.salute.gov.it" not in content


class TestPatternsList:
    """I pattern non devono essere vuoti e devono funzionare."""

    def test_patterns_are_compiled(self):
        for p in BLOCKED_PATTERNS:
            assert p.search("https://www.dati.salute.gov.it/test.csv")

    def test_patterns_reject_other(self):
        for p in BLOCKED_PATTERNS:
            assert not p.search("https://www.istat.it/data.csv")
