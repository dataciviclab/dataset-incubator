"""Tests for get_extra_ca_cert_urls.py.

Contratto: get_urls() estrae URL extra_ca_cert_url/extra_ca_cert_urls da YAML.
Usato in fase di fetch raw per certificati CA aggiuntivi.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pytest

from get_extra_ca_cert_urls import get_urls


@pytest.mark.contract
class GetExtraCaCertUrlsTest(unittest.TestCase):
    """Fail-fast su YAML/config invalida, tollerante su file mancante."""

    def test_missing_file_returns_empty(self) -> None:
        self.assertEqual(get_urls(Path("/nonexistent/dataset.yml")), [])

    def test_no_extra_ca_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "dataset.yml"
            cfg.write_text("dataset:\n  name: Test\n")
            self.assertEqual(get_urls(cfg), [])

    def test_single_url(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "dataset.yml"
            cfg.write_text("""
raw:
  sources:
    - args:
        extra_ca_cert_url: https://example.test/cert.crt
""")
            self.assertEqual(get_urls(cfg), ["https://example.test/cert.crt"])

    def test_multiple_urls_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "dataset.yml"
            cfg.write_text("""
raw:
  sources:
    - args:
        extra_ca_cert_urls:
          - https://example.test/a.crt
          - https://example.test/b.crt
          - https://example.test/a.crt
""")
            self.assertEqual(
                get_urls(cfg),
                [
                    "https://example.test/a.crt",
                    "https://example.test/b.crt",
                ],
            )

    def test_malformed_yaml_raises(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            cfg = Path(td) / "dataset.yml"
            cfg.write_text("invalid: [yaml: bad")
            with self.assertRaises(Exception):
                get_urls(cfg)


if __name__ == "__main__":
    unittest.main()
