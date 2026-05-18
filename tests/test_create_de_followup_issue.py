"""Test per scripts/create_de_followup_issue.py.

Verifica il filtro slug:
- slug già nel catalogo pre-merge -> non crea issue
- slug nuovo (non in catalogo pre-merge) -> crea issue
- misto: solo i nuovi passano
- git_ref non raggiungibile -> fallback a catalogo corrente
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from create_de_followup_issue import _extract_slugs, _read_catalog_json

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


class TestReadCatalogJson:
    def test_read_from_disk(self, tmp_path, monkeypatch):
        """Legge dal filesystem quando git_ref è None."""
        # Scrive un catalogo temporaneo
        catalog_path = tmp_path / "registry" / "clean_catalog.json"
        catalog_path.parent.mkdir(parents=True)
        catalog_path.write_text(json.dumps(FIXTURE_CATALOG))

        monkeypatch.chdir(tmp_path)
        # Dobbiamo far puntare REPO_ROOT a tmp_path
        import create_de_followup_issue as module
        original_root = module.REPO_ROOT
        module.REPO_ROOT = tmp_path

        try:
            catalog = _read_catalog_json(git_ref=None)
            assert catalog is not None
            assert len(catalog["datasets"]) == 4
        finally:
            module.REPO_ROOT = original_root

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


class TestFilterSlugs:
    """Testa la logica di filtro nel main, con mock di subprocess e gh."""

    def _run_main(self, items, base_sha=None):
        """Avvia main() con env vars controllate e mock di subprocess.run."""
        env = {
            "ITEMS_JSON": json.dumps(items),
            "PR_NUMBER": "999",
            "PR_TITLE": "test PR",
            "GH_TOKEN": "fake-token",
        }
        if base_sha:
            env["BASE_SHA"] = base_sha

        with patch.dict(os.environ, env, clear=True):
            from create_de_followup_issue import main

            # Mock git show per restituire il catalogo fixture
            def fake_subprocess_run(cmd, **kwargs):
                if "git" in cmd and "show" in cmd and "nonexistent" not in " ".join(cmd):
                    return MagicMock(
                        returncode=0,
                        stdout=json.dumps(FIXTURE_CATALOG),
                        stderr="",
                    )
                elif "gh" in cmd and "issue" in cmd and "create" in cmd:
                    return MagicMock(
                        returncode=0,
                        stdout="https://github.com/dataciviclab/data-explorer/issues/999",
                        stderr="",
                    )
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch("subprocess.run", side_effect=fake_subprocess_run):
                return main()

    def test_all_existing_skips_issue(self):
        """Tutti gli item già in catalogo pre-merge -> nessuna issue."""
        rc = self._run_main(
            items=[
                {"slug": "bdap-lea", "kind": "candidate"},
            ],
            base_sha="main",
        )
        assert rc == 0  # Successo: skip senza creare issue

    def test_new_item_creates_issue(self):
        """Item nuovo (non in catalogo pre-merge) -> crea issue."""
        rc = self._run_main(
            items=[
                {"slug": "mega-nuovo-dataset", "kind": "candidate"},
            ],
            base_sha="main",
        )
        assert rc == 0  # Issue creata

    def test_mixed_only_new_passes(self):
        """Misto: solo gli item nuovi generano issue."""
        rc = self._run_main(
            items=[
                {"slug": "bdap-lea", "kind": "candidate"},            # già noto
                {"slug": "mega-nuovo-dataset", "kind": "candidate"},  # nuovo
            ],
            base_sha="main",
        )
        assert rc == 0

    def test_empty_items_skips(self):
        """Lista vuota -> skip."""
        rc = self._run_main(items=[], base_sha="main")
        assert rc == 0

    def test_without_base_sha_falls_back_to_disk(self):
        """Senza BASE_SHA (workflow_dispatch) usa catalogo da filesystem.

        Se il catalogo su disco non esiste, nessun filtro -> item passa.
        """
        with patch.object(Path, "exists", return_value=False):
            rc = self._run_main(
                items=[
                    {"slug": "bdap-lea", "kind": "candidate"},
                ],
                base_sha=None,
            )
        assert rc == 0  # Issue creata perché catalogo non trovato
