"""Crea una issue su un repo GitHub per nuovi dataset pubblicati.

Usage (env vars):
  REPO         repo target: "dataciviclab/dataciviclab" o "dataciviclab/data-explorer"
  ITEMS_JSON   JSON array di items con slug (solo nuovi, filtro gia' applicato)
  PR_NUMBER    numero della PR mergiata (opzionale)
  PR_TITLE     titolo della PR mergiata (opzionale)
  GH_TOKEN     token GitHub con scope issues:write sul repo target
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

_REPO_CONFIG: dict[str, dict] = {
    "dataciviclab/dataciviclab": {
        "label": "analisi",
        "per_item": True,
        "title": lambda slug, items, pr_ref, pr_number: (
            f"analisi: {slug} — nuovo dataset pubblicato"
        ),
        "body": lambda slug, items, pr_ref, pr_number: (
            f"## Nuovo dataset pronto per analisi\n\n"
            f"Il dataset `{slug}` e' stato aggiunto al catalogo "
            f"({pr_ref}).\n\n"
            f"### Dati disponibili\n\n"
            f"- **Contratto tecnico**: candidates/{slug}/ in dataset-incubator\n"
            f"- **Parquet (se GCS OK)**: `gs://dataciviclab-clean/{slug}/`\n"
            f"- **Catalogo**: {slug} in registry/registry.json\n\n"
            f"### Prossimo passo\n\n"
            f"Usare [new-analysis](https://github.com/dataciviclab/dataciviclab/blob/main/skills/new-analysis.md) "
            f"per aprire un'analisi in `dataciviclab/analisi/{slug}/`:\n\n"
            f"1. Branch `feat/{slug}` da main in dataciviclab\n"
            f"2. Notebook + README + figure seguendo il template\n"
            f"3. PR verso main\n\n"
            f"### Riferimenti\n\n"
            f"- PR dataset-incubator #{pr_number}"
        ),
    },
    "dataciviclab/data-explorer": {
        "label": "curation",
        "per_item": False,
        "title": lambda slug, items, pr_ref, pr_number: (
            f"follow-up: pagina e tema per {items[0]['slug']}"
            if len(items) == 1
            else f"follow-up: pagina e tema per {len(items)} nuovi dataset"
        ),
        "body": lambda slug, items, pr_ref, pr_number: (
            f"## Nuovo/i dataset pubblicato/i\n\n"
            f"Il seguente/i dataset sono stati aggiunti al catalogo tecnico da "
            f"{pr_ref}.\n"
            f"Sono in catalogo ma **mancano di pagina curata e tema**.\n\n"
            f"### Da fare\n\n"
            + "\n".join(
                f"- [ ] {i['slug']}: aggiungere tema in src/data/themes.json.py (data-explorer) "
                f"e creare pagina dataset"
                for i in items
            )
            + f"\n\n### Workflow\n\n"
            f"1. Aggiungere/modificare in `src/data/themes.json.py` in data-explorer "
            f"(decisione editoriale)\n"
            f"2. Creare pagina dataset in data-explorer con query curate\n\n"
            f"### Riferimenti\n\n"
            f"- PR dataset-incubator #{pr_number}"
        ),
    },
}


def main() -> int:
    repo = os.environ.get("REPO", "")
    if repo not in _REPO_CONFIG:
        print(
            f"ERRORE: REPO deve essere uno di {list(_REPO_CONFIG.keys())}",
            file=sys.stderr,
        )
        return 1

    config = _REPO_CONFIG[repo]
    items_raw = os.environ.get("ITEMS_JSON", "[]")
    pr_number = os.environ.get("PR_NUMBER", "")
    pr_title = os.environ.get("PR_TITLE", "")
    pr_ref = f"#{pr_number}" if pr_number else pr_title if pr_title else "?"

    try:
        items = json.loads(items_raw)
    except json.JSONDecodeError:
        print("ERRORE: ITEMS_JSON non valido", file=sys.stderr)
        return 1

    if not items:
        print("Nessun item — skip")
        return 0

    if config["per_item"]:
        # Un'issue per slug (es. dataciviclab)
        for item in items:
            slug = item.get("slug", "?")
            title = config["title"](slug, items, pr_ref, pr_number)
            body = config["body"](slug, items, pr_ref, pr_number)
            rc = _create_issue(repo, config["label"], title, body)
            if rc != 0:
                return rc
    else:
        # Un'unica issue per tutti gli slug (es. data-explorer)
        slug = items[0].get("slug", "?")
        title = config["title"](slug, items, pr_ref, pr_number)
        body = config["body"](slug, items, pr_ref, pr_number)
        rc = _create_issue(repo, config["label"], title, body)
        if rc != 0:
            return rc

    return 0


def _create_issue(repo: str, label: str, title: str, body: str) -> int:
    result = subprocess.run(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--label",
            label,
            "--body",
            body,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERRORE creazione issue in {repo}: {result.stderr}", file=sys.stderr)
        return 1

    print(f"Issue creata in {repo}: {result.stdout.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
