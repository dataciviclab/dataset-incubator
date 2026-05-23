"""Crea una issue in dataciviclab per avviare l'analisi di un nuovo dataset.

Si attiva dopo il post-merge, solo per dataset appena pubblicati (non già
presenti nel catalogo pre-merge).

Usage (env vars):
  ITEMS_JSON  JSON array di items con slug
  PR_NUMBER   numero della PR mergiata
  PR_TITLE    titolo della PR mergiata
  BASE_SHA    (opzionale) SHA del base branch prima del merge.
              Se omesso (es. workflow_dispatch), confronta col catalogo
              corrente su filesystem.
  GH_TOKEN    token GitHub con scope issues:write su dataciviclab
"""

import json
import os
import subprocess
import sys

from _catalog_helpers import load_catalog_slugs


def main() -> int:
    items_raw = os.environ.get("ITEMS_JSON", "[]")
    pr_number = os.environ.get("PR_NUMBER", "?")
    pr_title = os.environ.get("PR_TITLE", "?")

    try:
        items = json.loads(items_raw)
    except json.JSONDecodeError:
        print("ERRORE: ITEMS_JSON non valido", file=sys.stderr)
        return 1

    if not items:
        print("Nessun item — skip")
        return 0

    # Filtra item già presenti nel catalogo pre-merge
    known_slugs = load_catalog_slugs(git_ref=os.environ.get("BASE_SHA"))
    new_items = [i for i in items if i.get("slug") not in known_slugs] if known_slugs else items

    if not new_items:
        print(f"Tutti gli item ({len(items)}) sono già presenti nel catalogo pre-merge — nessuna issue DCL creata")
        return 0

    # Body
    for item in new_items:
        slug = item.get("slug", "?")
        root = item.get("root", "candidates")
        title = f"analisi: {slug} — nuovo dataset pubblicato"

        body = (
            f"## Nuovo dataset pronto per analisi\n\n"
            f"Il dataset `{slug}` è stato pubblicato automaticamente da "
            f"PR #{pr_number} — {pr_title}.\n\n"
            f"### Dati disponibili\n\n"
            f"- **Contratto tecnico**: `{root}/{slug}/` in dataset-incubator\n"
            f"- **Parquet pubblici**: `gs://dataciviclab-clean/{slug}/`\n"
            f"- **Catalogo**: {slug} in registry/clean_catalog.json\n\n"
            f"### Prossimo passo\n\n"
            f"Usare [new-analysis](https://github.com/dataciviclab/dataciviclab/blob/main/skills/new-analysis.md) "
            f"per aprire un'analisi in `dataciviclab/analisi/{slug}/`:\n\n"
            f"1. Branch `feat/{slug}` da main in dataciviclab\n"
            f"2. Notebook + README + figure seguendo il template\n"
            f"3. PR verso main\n\n"
            f"### Riferimenti\n\n"
            f"- PR dataset-incubator #{pr_number}"
        )

        result = subprocess.run(
            [
                "gh", "issue", "create",
                "--repo", "dataciviclab/dataciviclab",
                "--title", title,
                "--label", "analisi",
                "--body", body,
            ],
            capture_output=True, text=True,
        )

        if result.returncode != 0:
            print(f"ERRORE creazione issue per {slug}: {result.stderr}", file=sys.stderr)
            return 1

        print(f"Issue creata per {slug}: {result.stdout.strip()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
