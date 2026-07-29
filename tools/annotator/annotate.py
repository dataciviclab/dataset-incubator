#!/usr/bin/env python3
"""
annotate.py — Assegna tipi semantici alle colonne del catalogo.

Legge:
  - registry/clean_catalog.json  (dataset, colonne)
  - registry/semantic_types.yaml (vocabolario)

Produce:
  - registry/catalog_annotated.json  (stesso catalogo + semantic_type per colonna)

Uso::

    python tools/annotator/annotate.py [--json]
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

DI_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = DI_ROOT / "registry" / "clean_catalog.json"
SEMTYPES_PATH = DI_ROOT / "registry" / "semantic_types.yaml"
OUTPUT_PATH = DI_ROOT / "registry" / "catalog_annotated.json"


def load_catalog() -> list[dict]:
    data = json.loads(CATALOG_PATH.read_text())
    return data.get("datasets", data if isinstance(data, list) else [])


def load_semantic_types() -> dict[str, dict]:
    data = yaml.safe_load(SEMTYPES_PATH.read_text())
    return {stype: info for stype, info in data.get("types", {}).items()}


def _build_alias_map(types: dict[str, dict]) -> dict[str, str]:
    """Costruisce mappa alias → semantic_type_name."""
    alias_map = {}
    for stype, info in types.items():
        for alias in info.get("aliases", []):
            alias_lower = alias.lower()
            # Se conflitto, il tipo con peso maggiore vince
            existing = alias_map.get(alias_lower)
            if existing:
                existing_weight = types[existing].get("weight", 0)
                new_weight = info.get("weight", 0)
                if new_weight > existing_weight:
                    alias_map[alias_lower] = stype
            else:
                alias_map[alias_lower] = stype
    return alias_map


def annotate_catalog() -> list[dict]:
    catalog = load_catalog()
    types = load_semantic_types()
    alias_map = _build_alias_map(types)

    stats = {"total_datasets": len(catalog), "annotated_columns": 0, "unannotated_columns": 0}

    for ds in catalog:
        for col in ds.get("columns", []):
            col_name = col.get("name", "")
            col_lower = col_name.lower()

            # Match esatto con alias
            semantic_type = alias_map.get(col_lower)

            # Se non trovato, prova partial match SOLO per alias lunghi (≥6)
            # Alias corti (<6) generano falsi positivi: "prov" in "provvedimento",
            # "ipa" in "partecipazione", "stato" in "stato_opera", ecc.
            if not semantic_type:
                for stype, info in types.items():
                    for alias in info.get("aliases", []):
                        if len(alias) >= 6 and alias.lower() in col_lower:
                            semantic_type = stype
                            break
                    if semantic_type:
                        break

            if semantic_type:
                col["semantic_type"] = semantic_type
                stats["annotated_columns"] += 1
            else:
                stats["unannotated_columns"] += 1

    print(f"Dataset: {stats['total_datasets']}")
    print(f"Colonne annotate: {stats['annotated_columns']}")
    print(f"Colonne senza tipo: {stats['unannotated_columns']}")
    print(
        f"Copertura: {stats['annotated_columns'] / (stats['annotated_columns'] + stats['unannotated_columns']) * 100:.1f}%"
        if (stats["annotated_columns"] + stats["unannotated_columns"]) > 0
        else "N/A"
    )

    return catalog


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Annota il catalogo con tipi semantici")
    parser.add_argument("--json", action="store_true", help="Output JSON invece di scrivere file")
    args = parser.parse_args()

    catalog = annotate_catalog()

    if args.json:
        print(json.dumps(catalog, indent=2, ensure_ascii=False))
    else:
        OUTPUT_PATH.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "source": "clean_catalog.json",
                    "semantic_vocabulary": "semantic_types.yaml",
                    "datasets": catalog,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        print(f"Scritto {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
