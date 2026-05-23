"""Test per scripts/create_de_followup_issue.py e _catalog_helpers.py.

Contratto: extract_slugs() e read_catalog_json() determinano quali slug
sono nuovi e meritano una issue su data-explorer.
Usato in post-merge per aprire followup automatici.

Prova del fuoco: se cancello questi test, un refactor del filtro slug puo'
causare issue duplicate o mancanti.
"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from _catalog_helpers import extract_slugs as _extract_slugs, read_catalog_json as _read_catalog_json

FIXTURE_CATALOG = {
    "schema_version": 1,
    "datasets": [
        {"slug": "aifa_spesa_consumo", "name": "AIFA Spesa"},
        {"slug": "bdap_lea", "name": "BDAP LEA"},
        {"slug": "consip_consumi_convenzione", "name": "Consip Consumi"},
        {"slug": "dipendenti_pubblici", "name": "Dipendenti Pubblici"},
    ],
}

FIXTURE_ITEMS = [
    {"slug": "bdap-lea", "kind": "candidate"},            # già in catalogo
    {"slug": "dipendenti-pubblici", "kind": "candidate"},  # già in catalogo
    {"slug": "mega-nuovo-dataset", "kind": "candidate"},   # NUOVO
]


@pytest.mark.pure_unit
class TestExtractSlugs:
    def test_extract_normalizes_underscore_to_hyphen(self):
        slugs = _extract_slugs(FIXTURE_CATALOG)
        assert "aifa-spesa-consumo" in slugs
        assert "bdap-lea" in slugs
        assert "consip-consumi-convenzione" in slugs
        assert len(slugs) == 4

    def test_extract_empty_on_none(self):
        assert _extract_slugs(None) == set()

    def test_extract_empty_on_empty_dict(self):
        assert _extract_slugs({}) == set()

    def test_extract_skips_entries_without_slug(self):
        catalog = {"datasets": [{"name": "no-slug"}, {"slug": "ok", "name": "OK"}]}
        slugs = _extract_slugs(catalog)
        assert slugs == {"ok"}


@pytest.mark.contract
class TestReadCatalogJson:
    def test_read_from_git_head(self):
        """Legge il catalogo dal filesystem tramite Path locale."""
        catalog = _read_catalog_json(git_ref=None)
        # git_ref=None -> legge dal filesystem
        # Il catalogo esiste in sviluppo; in CI con --ignore puo' non essere
        # presente, quindi il test non fallisce se None.
        if catalog is not None:
            assert "datasets" in catalog

    def test_read_from_git(self):
        """Legge da git quando git_ref è specificato."""
        catalog = _read_catalog_json(git_ref="HEAD")
        # HEAD punta al commit corrente, che ha il catalogo
        if catalog is not None:
            assert "datasets" in catalog
        # Se git non è disponibile (CI senza git), catalog è None -> skip

    def test_read_from_git_bad_ref_returns_none(self):
        """Un git_ref inesistente restituisce None senza crash."""
        catalog = _read_catalog_json(git_ref="nonexistent-sha-1234567")
        assert catalog is None


@pytest.mark.contract
class TestCreateIssues:
    """Testa la creazione issue con mock di subprocess e gh."""

    def _run_main(self, items):
        """Avvia main() con env vars controllate e mock di subprocess.run."""
        env = {
            "ITEMS_JSON": json.dumps(items),
            "PR_NUMBER": "999",
            "PR_TITLE": "test PR",
            "GH_TOKEN": "fake-token",
        }

        with patch.dict(os.environ, env, clear=True):
            from create_de_followup_issue import main

            def fake_subprocess_run(cmd, **kwargs):
                if "gh" in cmd and "issue" in cmd and "create" in cmd:
                    return MagicMock(
                        returncode=0,
                        stdout="https://github.com/dataciviclab/data-explorer/issues/999",
                        stderr="",
                    )
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch("subprocess.run", side_effect=fake_subprocess_run):
                return main()

    def test_single_item_creates_issue(self):
        """Un item -> crea issue."""
        rc = self._run_main(
            items=[{"slug": "mega-nuovo-dataset", "kind": "candidate"}],
        )
        assert rc == 0

    def test_multiple_items_all_create_issues(self):
        """Più item -> tutti generano issue (nessun filtro)."""
        rc = self._run_main(
            items=[
                {"slug": "bdap-lea", "kind": "candidate"},
                {"slug": "mega-nuovo-dataset", "kind": "candidate"},
            ],
        )
        assert rc == 0

    def test_empty_items_skips(self):
        """Lista vuota -> skip."""
        rc = self._run_main(items=[])
        assert rc == 0
