"""Crea una issue di follow-up in data-explorer per nuovi dataset pubblicati.

Filtra gli slug già presenti nel catalogo pulito **prima del merge**
(``BASE_SHA``), non dopo. In questo modo:
- un nuovo dataset appena pubblicato genera regolarmente la issue DE
- una PR tecnica su un dataset già noto non genera rumore

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
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # dataset-incubator/


def _read_catalog_json(git_ref: str | None = None) -> dict | None:
    """Legge il catalogo pulito e restituisce il dict parsato, o None.

    Se ``git_ref`` è specificato, legge da git (alberino pre-merge).
    Altrimenti legge dal filesystem.
    """
    if git_ref:
        try:
            result = subprocess.run(
                ["git", "show", f"{git_ref}:registry/clean_catalog.json"],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            if result.returncode != 0:
                print(
                    f"AVVISO: git show {git_ref}:registry/clean_catalog.json "
                    f"fallito ({result.stderr.strip()})"
                )
                return None
            return json.loads(result.stdout)
        except (json.JSONDecodeError, subprocess.CalledProcessError) as exc:
            print(f"AVVISO: impossibile leggere catalogo da git@{git_ref}: {exc}")
            return None

    # Filesystem
    catalog_path = REPO_ROOT / "registry" / "clean_catalog.json"
    if not catalog_path.exists():
        print(f"AVVISO: {catalog_path} non trovato — nessun filtro applicato")
        return None
    try:
        return json.loads(catalog_path.read_text())
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"AVVISO: impossibile leggere {catalog_path}: {exc}")
        return None


def _extract_slugs(catalog: dict | None) -> set[str]:
    """Estrae gli slug normalizzati (trattini) da un dict catalogo."""
    if not catalog:
        return set()
    return {
        entry["slug"].replace("_", "-")
        for entry in catalog.get("datasets", [])
        if "slug" in entry
    }


def _load_catalog_slugs(git_ref: str | None = None) -> set[str]:
    """Carica gli slug dal catalogo pulito e restituisce un set.

    Se ``git_ref`` è specificato, legge il catalogo da git (pre-merge).
    Altrimenti legge dal filesystem (catalogo corrente, eventualmente
    già aggiornato dal post-merge pipeline).

    Gli slug nel catalogo usano underscore (``aifa_spesa_consumo``),
    mentre gli item di detect usano trattini (``aifa-spesa-consumo``).
    Normalizza tutto a trattini per il confronto.
    """
    catalog = _read_catalog_json(git_ref=git_ref)
    slugs = _extract_slugs(catalog)
    source = f"git@{git_ref[:12]}" if git_ref else "filesystem"
    print(f"DEBUG: {len(slugs)} slug noti dal catalogo ({source})")
    return slugs


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
    known_slugs = _load_catalog_slugs(git_ref=base_sha)
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
