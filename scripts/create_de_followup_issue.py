"""Crea una issue di follow-up in data-explorer per nuovi dataset pubblicati.

Usage (env vars):
  ITEMS_JSON  JSON array di items con slug (solo nuovi, filtro già applicato)
  PR_NUMBER   numero della PR mergiata (opzionale)
  PR_TITLE    titolo della PR mergiata (opzionale)
  GH_TOKEN    token GitHub con scope issues:write su data-explorer
"""

import json
import os
import subprocess
import sys


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

    # Costruisci lista items
    item_lines = "\n".join(
        f"- [ ] {i['slug']}: aggiungere tema in src/data/themes.json.py (data-explorer) e creare pagina dataset"
        for i in items
    )

    # Titolo
    if len(items) == 1:
        title = f"follow-up: pagina e tema per {items[0]['slug']}"
    else:
        title = f"follow-up: pagina e tema per {len(items)} nuovi dataset"

    # Body
    body = (
        f"## Nuovo/i dataset pubblicato/i\n\n"
f"Il seguente/i dataset sono stati aggiunti al catalogo tecnico da "
f"PR #{pr_number} — {pr_title}.\n"
f"Sono in catalogo ma **mancano di pagina curata e tema**.\n\n"
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
