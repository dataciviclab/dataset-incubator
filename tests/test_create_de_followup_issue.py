"""Test per scripts/create_de_followup_issue.py.

Contratto: su ITEMS_JSON in env, crea issue su data-explorer via gh CLI.
Usato in post-merge per aprire followup automatici per nuovi slug.
"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.contract


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
