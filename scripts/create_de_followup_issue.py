"""Crea una issue di follow-up in data-explorer per nuovi dataset pubblicati.

Filtra gli slug già presenti in ``registry/clean_catalog.json``:
se un dataset è già nel catalogo tecnico, non serve una nuova issue DE.

Usage (env vars):
  ITEMS_JSON  JSON array di items con slug
  PR_NUMBER   numero della PR mergiata
  PR_TITLE    titolo della PR mergiata
  GH_TOKEN    token GitHub con scope issues:write su data-explorer
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # dataset-incubator/


def _load_catalog_slugs() -> set[str]:
    """Carica gli slug dal catalogo pulito e restituisce un set.

    Gli slug nel catalogo usano underscore (``aifa_spesa_consumo``),
    mentre gli item di detect usano trattini (``aifa-spesa-consumo``).
    Normalizza tutto a trattini per il confronto.
    """
    catalog_path = REPO_ROOT / "registry" / "clean_catalog.json"
    if not catalog_path.exists():
        print(f"AVVISO: {catalog_path} non trovato — nessun filtro applicato")
        return set()

    try:
        data = json.loads(catalog_path.read_text())
        # La struttura ha una lista "datasets" con campo "slug"
        slugs = {
            entry["slug"].replace("_", "-")
            for entry in data.get("datasets", [])
            if "slug" in entry
        }
        print(f"DEBUG: {len(slugs)} slug noti dal catalogo pulito")
        return slugs
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"AVVISO: impossibile leggere {catalog_path}: {exc}")
        return set()


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

    # Filtra item già presenti nel catalogo pulito
    known_slugs = _load_catalog_slugs()
    new_items = [i for i in items if i.get("slug") not in known_slugs]

    if not new_items:
        print(
            f"Tutti gli item ({len(items)}) sono già presenti nel catalogo — "
            f"nessuna issue DE creata"
        )
        return 0

    skipped = len(items) - len(new_items)
    if skipped:
        print(f"Saltati {skipped} item già in catalogo")

    # Costruisci lista items
    item_lines = "\n".join(
        f"- [ ] {i['slug']}: aggiungere a themes.json e creare pagina dataset"
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
        f"1. Aggiungere a `catalog/themes.json` (decisione editoriale)\n"
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
