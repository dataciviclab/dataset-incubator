#!/usr/bin/env python3
"""
build_graph.py — Genera il grafo entità → dataset dal catalogo clean.

Legge registry/clean_catalog.json (con annotazioni semantic_type) e produce
entity_graph.json: un grafo dove i nodi sono entità (Comune, Provincia, Ente...)
e gli archi sono dataset che le descrivono, con bridge tra entità.

Uso::

    python tools/graph/build_graph.py [--json] [--entity Comune]

Dipende da: clean_catalog.json (con colonne annotate da build_clean_catalog.py --derive).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

DI_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = DI_ROOT / "registry" / "clean_catalog.json"
SEMTYPES_PATH = DI_ROOT / "registry" / "semantic_types.yaml"
OUTPUT_PATH = DI_ROOT / "registry" / "entity_graph.json"

# Entity display names
ENTITY_LABELS = {
    "Comune": "Comune (ISTAT)",
    "Ente": "Ente pubblico",
    "Provincia": "Provincia",
    "Regione": "Regione",
    "Scuola": "Scuola",
    "Gara": "Gara / Appalto",
    "Progetto": "Progetto",
    "Impresa": "Impresa",
    "Nazione": "Nazione",
    "Tempo": "Tempo / data",
    "Attività economica": "Attività economica",
    "Stazione Appaltante": "Stazione Appaltante",
    "Ente sanitario": "Ente sanitario",
    "Procedimento": "Procedimento giudiziario",
    "Categoria merceologica": "Categoria merceologica",
}


def load_annotated() -> list[dict]:
    data = json.loads(CATALOG_PATH.read_text())
    return data.get("datasets", data if isinstance(data, list) else [])


def load_semantic_types() -> dict[str, dict]:
    data = yaml.safe_load(SEMTYPES_PATH.read_text())
    return data.get("types", {})


def build_graph() -> dict:
    datasets = load_annotated()
    types_info = load_semantic_types()

    # Nodi: entity → { datasets: [...], types: {...} }
    nodes: dict[str, dict] = {}
    # Relazioni: tra entity (da bridge)
    relations: list[dict] = []

    for ds in datasets:
        slug = ds["slug"]
        ds_name = ds.get("name", slug)

        for col in ds.get("columns", []):
            st = col.get("semantic_type")
            if not st:
                continue

            type_info = types_info.get(st, {})
            entity = type_info.get("entity", "Sconosciuto")

            if entity not in nodes:
                nodes[entity] = {
                    "entity": entity,
                    "label": ENTITY_LABELS.get(entity, entity),
                    "datasets": [],
                    "types": {},
                }

            # Aggiungi dataset alla lista
            ds_entry = {
                "slug": slug,
                "name": ds_name,
                "column": col["name"],
                "semantic_type": st,
            }

            # Evita duplicati (stesso slug + stesso tipo + stessa colonna)
            existing = [
                d
                for d in nodes[entity]["datasets"]
                if d["slug"] == slug and d["column"] == col["name"]
            ]
            if not existing:
                nodes[entity]["datasets"].append(ds_entry)

            # Conta tipi
            if st not in nodes[entity]["types"]:
                nodes[entity]["types"][st] = 0
            nodes[entity]["types"][st] += 1

            # Se il tipo ha un bridge, genera relazione
            bridge = type_info.get("bridge")
            if bridge:
                via = bridge.get("via", "")
                on = bridge.get("on", "")
                to_st = bridge.get("to", "")
                to_info = types_info.get(to_st, {})
                to_entity = to_info.get("entity", "Sconosciuto")

                if to_entity and to_entity != entity:
                    relations.append(
                        {
                            "from": {"entity": entity, "dataset": slug, "via": st},
                            "to": {
                                "entity": to_entity,
                                "bridge": via,
                                "on": on,
                                "semantic_type": to_st,
                            },
                        }
                    )

    # Ordina dataset per slug
    for entity in nodes:
        nodes[entity]["datasets"].sort(key=lambda d: d["slug"])

    return {
        "schema_version": 1,
        "generated_from": "clean_catalog.json",
        "entities": {e: info for e, info in sorted(nodes.items())},
        "bridges": relations,
        "summary": {
            "total_entities": len(nodes),
            "total_relations": len(relations),
        },
    }


def _print_graph(graph: dict, filter_entity: str | None = None):
    entities = graph["entities"]

    if filter_entity:
        entities = {k: v for k, v in entities.items() if k.lower() == filter_entity.lower()}

    for entity, info in sorted(entities.items()):
        print(f"\n{'═' * 60}")
        print(f"  {info['label']} ({entity})")
        print(f"  Tipi: {', '.join(f'{k}({v})' for k, v in sorted(info['types'].items()))}")
        print(f"  Dataset ({len(info['datasets'])}):")

        for ds in info["datasets"]:
            bridge_info = ""
            for rel in graph.get("bridges", []):
                if rel["from"]["dataset"] == ds["slug"] and rel["from"]["entity"] == entity:
                    bridge_info = f" → [{rel['to']['bridge']}] → {rel['to']['entity']}"
            print(
                f"    • {ds['slug']:<35} via {ds['semantic_type']:<20} (col: {ds['column']}){bridge_info}"
            )

    # Bridges
    bridges = graph.get("bridges", [])
    if bridges and not filter_entity:
        print(f"\n{'═' * 60}")
        print(f"  BRIDGE ({len(bridges)}):")
        for rel in bridges:
            print(
                f"    {rel['from']['entity']} ← {rel['from']['dataset']}.{rel['from']['via']} → {rel['to']['bridge']}.{rel['to']['on']} → {rel['to']['entity']}.{rel['to']['semantic_type']}"
            )

    print(f"\n{'═' * 60}")
    print(
        f"  Riepilogo: {graph['summary']['total_entities']} entità, {graph['summary']['total_relations']} bridge"
    )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Genera il grafo entità → dataset")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--entity", type=str, default=None, help="Filtra per entità (es. Comune)")
    args = parser.parse_args()

    graph = build_graph()

    if args.json:
        print(json.dumps(graph, indent=2, ensure_ascii=False))
    else:
        _print_graph(graph, args.entity)

    # Salva sempre
    OUTPUT_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
