"""Helper condivisi per leggere e filtrare slug da clean_catalog.json.

Usati da create_de_followup_issue.py e create_dcl_analysis_issue.py.
"""

import json
import subprocess
from pathlib import Path


def read_catalog_json(git_ref: str | None = None) -> dict | None:
    """Legge clean_catalog.json e restituisce il dict parsato, o None.

    Se ``git_ref`` è specificato, legge da git (alberino pre-merge).
    Altrimenti legge dal filesystem (catalogo corrente).
    """
    repo_root = Path(__file__).resolve().parent.parent

    if git_ref:
        try:
            result = subprocess.run(
                ["git", "show", f"{git_ref}:registry/clean_catalog.json"],
                capture_output=True,
                text=True,
                cwd=repo_root,
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
    catalog_path = repo_root / "registry" / "clean_catalog.json"
    if not catalog_path.exists():
        print(f"AVVISO: {catalog_path} non trovato — nessun filtro applicato")
        return None
    try:
        return json.loads(catalog_path.read_text())
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"AVVISO: impossibile leggere {catalog_path}: {exc}")
        return None


def extract_slugs(catalog: dict | None) -> set[str]:
    """Estrae gli slug normalizzati (trattini) da un dict catalogo."""
    if not catalog:
        return set()
    return {
        entry["slug"].replace("_", "-") for entry in catalog.get("datasets", []) if "slug" in entry
    }


def load_catalog_slugs(git_ref: str | None = None) -> set[str]:
    """Carica gli slug dal catalogo pulito e restituisce un set.

    Se ``git_ref`` è specificato, legge il catalogo da git (pre-merge).
    Altrimenti legge dal filesystem (catalogo corrente).

    Gli slug nel catalogo usano underscore (``aifa_spesa_consumo``).
    Normalizza tutto a trattini per il confronto.
    """
    catalog = read_catalog_json(git_ref=git_ref)
    slugs = extract_slugs(catalog)
    source = f"git@{git_ref[:12]}" if git_ref else "filesystem"
    print(f"DEBUG: {len(slugs)} slug noti dal catalogo ({source})")
    return slugs
