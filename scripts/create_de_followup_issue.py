"""Crea una issue di follow-up in data-explorer per nuovi dataset pubblicati.

Usage (env vars):
  ITEMS_JSON  JSON array di items con slug
  PR_NUMBER   numero della PR mergiata
  PR_TITLE    titolo della PR mergiata
  BASE_SHA    (opzionale) SHA del base branch prima del merge.
              Se omesso (es. workflow_dispatch), confronta col catalogo
              corrente su filesystem.
  GH_TOKEN    token GitHub con scope issues:write su data-explorer
"""

import json
import os
import subprocess
import sys

from _catalog_helpers import extract_slugs, load_catalog_slugs


def main() -> int:
    items_raw = os.environ.get("ITEMS_JSON", "[]")
    pr_number = os.environ.get("PR_NUMBER", "?")
    pr_title = os.environ.get("PR_TITLE", "?")
    base_sha = os.environ.get("BASE_SHA", None)

    try:
        items = json.loads(items_raw)
    except json.JSONDecodeError:
        print("ERRORE: ITEMS_JSON non valido", file=sys.stderr)
        return 1

    if not items:
        print("Nessun item — skip")
        return 0

    # Filtra item già presenti nel catalogo **pre-merge** (base branch)
    known_slugs = load_catalog_slugs(git_ref=base_sha)
    # Se il catalogo non è stato leggibile, known_slugs sarà vuoto
    # e nessun filtro verrà applicato (tutti gli item passano)
    new_items = [i for i in items if i.get("slug") not in known_slugs] if known_slugs else items

    if not new_items:
        print(
            f"Tutti gli item ({len(items)}) sono già presenti nel catalogo "
            f"pre-merge — nessuna issue DE creata"
        )
        return 0

    skipped = len(items) - len(new_items)
    if skipped:
        print(f"Saltati {skipped} item già in catalogo pre-merge")

    # Costruisci lista items
    item_lines = "\n".join(
        f"- [ ] {i['slug']}: aggiungere tema in src/data/themes.json.py (data-explorer) e creare pagina dataset"
        for i in new_items
    )

    # Titolo
    if len(new_items) == 1:
        title = f"follow-up: pagina e tema per {new_items[0]['slug']}"
    else:
        title = f"follow-up: pagina e tema per {len(new_items)} nuovi dataset"

    # Body
    body = (
        f"## Nuovo/i dataset pubblicato/i\n\n"
        f"Il seguente/i dataset sono stati pubblicati automaticamente da "
        f"PR #{pr_number} — {pr_title}.\n"
        f"Sono disponibili nel catalogo tecnico ma **mancano di pagina curata e tema**.\n\n"
        f"### Da fare\n\n{item_lines}\n\n"
        f"### Workflow\n\n"
        f"1. Aggiungere/modificare in `src/data/themes.json.py` in data-explorer (decisione editoriale)\n"
        f"2. Creare pagina dataset in data-explorer con query curate\n\n"
        f"### Riferimenti\n\n"
        f"- PR dataset-incubator #{pr_number}"
    )

    # Crea issue
    result = subprocess.run(
        [
            "gh", "issue", "create",
            "--repo", "dataciviclab/data-explorer",
            "--title", title,
            "--label", "curation",
            "--body", body,
        ],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print(f"ERRORE creazione issue: {result.stderr}", file=sys.stderr)
        return 1

    print(f"Issue creata: {result.stdout.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
