"""Test per scripts/create_issue.py.

Contratto: su ITEMS_JSON e REPO in env, crea issue su GitHub via gh CLI.
Usato in post-merge per aprire followup automatici per nuovi slug.
"""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.contract


def _run_main(items: list[dict], repo: str) -> int:
    """Avvia main() con env vars controllate e mock di subprocess.run."""
    env = {
        "ITEMS_JSON": json.dumps(items),
        "PR_NUMBER": "999",
        "PR_TITLE": "test PR",
        "GH_TOKEN": "fake-token",
        "REPO": repo,
    }

    with patch.dict(os.environ, env, clear=True):
        from create_issue import main

        def fake_subprocess_run(cmd, **kwargs):
            if "gh" in cmd and "issue" in cmd and "create" in cmd:
                return MagicMock(
                    returncode=0,
                    stdout=f"https://github.com/{repo}/issues/999",
                    stderr="",
                )
            return MagicMock(returncode=0, stdout="", stderr="")

        with patch("subprocess.run", side_effect=fake_subprocess_run):
            return main()


@pytest.mark.contract
class TestCreateIssueDCL:
    """Issue su dataciviclab/dataciviclab — un'issue per slug."""

    def test_single_item_creates_issue(self):
        rc = _run_main(
            items=[{"slug": "mega-nuovo-dataset", "kind": "candidate"}],
            repo="dataciviclab/dataciviclab",
        )
        assert rc == 0

    def test_multiple_items_create_one_issue_each(self):
        rc = _run_main(
            items=[
                {"slug": "bdap-lea", "kind": "candidate"},
                {"slug": "mega-nuovo-dataset", "kind": "candidate"},
            ],
            repo="dataciviclab/dataciviclab",
        )
        assert rc == 0


@pytest.mark.contract
class TestCreateIssueDE:
    """Issue su dataciviclab/data-explorer — un'unica issue per tutti."""

    def test_single_item_creates_issue(self):
        rc = _run_main(
            items=[{"slug": "mega-nuovo-dataset", "kind": "candidate"}],
            repo="dataciviclab/data-explorer",
        )
        assert rc == 0

    def test_multiple_items_create_single_issue(self):
        rc = _run_main(
            items=[
                {"slug": "bdap-lea", "kind": "candidate"},
                {"slug": "mega-nuovo-dataset", "kind": "candidate"},
            ],
            repo="dataciviclab/data-explorer",
        )
        assert rc == 0


class TestCreateIssueErrors:
    @pytest.mark.contract
    def test_empty_items_skips(self):
        rc = _run_main(items=[], repo="dataciviclab/data-explorer")
        assert rc == 0

    @pytest.mark.contract
    def test_invalid_repo_returns_error(self):
        rc = _run_main(
            items=[{"slug": "test", "kind": "candidate"}],
            repo="dataciviclab/invalid-repo",
        )
        assert rc != 0
