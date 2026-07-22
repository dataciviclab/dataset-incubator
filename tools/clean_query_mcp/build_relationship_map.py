"""Costruisce la mappa delle relazioni tra dataset.

Legge:
  - join_map.yaml       → relazioni territoriali (hub comuni_master)
  - relations-*.yaml    → relazioni di dominio (appalti, enti, giustizia, ...)

Produce una mappa con due sezioni:
  - registries: relazioni territoriali (hub → chiave → dataset) — per dataset_graph()
  - cross_relations: relazioni cross-dataset per dominio — per validazione e MART

Usata da dataset_graph() nel MCP server.

Uso::

    from clean_query_mcp.build_relationship_map import build
    mappa = build()
    mappa["registries"]        # relazioni territoriali
    mappa["cross_relations"]   # relazioni cross-dataset
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import glob as glob_mod

import yaml

DI_ROOT = Path(__file__).resolve().parents[2]
JOIN_MAP_PATH = DI_ROOT / "registry" / "join_map.yaml"
RELATIONS_DIR = DI_ROOT / "registry"


def _load_join_map() -> dict[str, Any]:
    with open(JOIN_MAP_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_relations_files() -> dict[str, Any]:
    """Carica tutti i relations-*.yaml e li restituisce come dict {domain: relazioni}."""
    relations = {}
    pattern = str(RELATIONS_DIR / "relations-*.yaml")
    for path in sorted(glob_mod.glob(pattern)):
        domain = path.split("relations-")[-1].replace(".yaml", "")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        rels = data.get("relations", [])
        if rels:
            relations[domain] = {
                "description": data.get("description", ""),
                "relations": rels,
            }
    return relations


def _build_registry_keys(data: dict[str, Any]) -> dict[str, Any]:
    """Costruisce la mappa invertita: da hub_key a lista di dataset."""
    hub = data.get("hub", {})
    hub_slug = hub.get("slug", "comuni_master")
    hub_keys = hub.get("keys", {})

    # Organizza: hub_key -> lista dataset
    by_key: dict[str, list[dict[str, Any]]] = {}

    for ds in data.get("datasets", []):
        # Salta gli hub stessi e i dataset non joinabili
        if ds.get("hub"):
            continue
        if ds.get("joinable_by_comune") is False:
            continue

        hub_key = ds.get("hub_key")
        if not hub_key or hub_key in ("~", None):
            continue

        if hub_key not in by_key:
            by_key[hub_key] = []

        ck = ds.get("comuni_key", {})
        normalizer = ds.get("normalizer", "direct")

        entry = {
            "slug": ds["slug"],
            "name": ds.get("name", ds["slug"]),
            "via": ck.get("column", "?"),
            "normalizer": normalizer,
            "granularity": ds.get("granularity", "?"),
            "year_column": ds.get("year_column"),
            "note": ds.get("note", ""),
        }
        by_key[hub_key].append(entry)

    # Costruisci output strutturato per registro
    registries = {}

    # comuni_master come hub principale
    keys_output = {}
    for key, datasets in sorted(by_key.items()):
        key_meta = hub_keys.get(key, {})
        keys_output[key] = {
            "description": key_meta.get("description", key),
            "datasets": sorted(datasets, key=lambda d: d["slug"]),
        }

    registries[hub_slug] = {
        "description": hub.get("description", "Golden record"),
        "hub": True,
        "keys": keys_output,
    }

    # bdap_anagrafe_enti come bridge (ha anche bridge_keys)
    for ds in data.get("datasets", []):
        if ds.get("slug") == "bdap_anagrafe_enti":
            bridge_keys = ds.get("bridge_keys", [])
            registries["bdap_anagrafe_enti"] = {
                "description": ds.get("note", "Bridge table IPA ↔ SIOPE ↔ ISTAT"),
                "hub": True,
                "bridge_keys": bridge_keys,
                "keys": {
                    "codice_istat_comune": {
                        "description": "Codice ISTAT del comune",
                        "datasets": [
                            {
                                "slug": "bdap_anagrafe_enti",
                                "name": "BDAP Anagrafe Enti",
                                "via": "codice_istat_comune",
                                "normalizer": "direct",
                                "granularity": "ente",
                                "note": "Mappa 38k enti con codici IPA, SIOPE, ISTAT, MIUR, catastale",
                            }
                        ],
                    }
                },
            }
            break

    return registries


def _find_unconnected(data: dict[str, Any]) -> list[dict[str, str]]:
    """Trova dataset che non hanno join per comune."""
    unconnected = []
    for ds in data.get("datasets", []):
        if ds.get("joinable_by_comune") is False:
            unconnected.append(
                {
                    "slug": ds["slug"],
                    "name": ds.get("name", ds["slug"]),
                    "granularity": ds.get("granularity", "?"),
                    "note": ds.get("note", ""),
                }
            )
    return unconnected


def _build_cross_relations(relations_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Appiattisce le relazioni da relations-*.yaml in una lista unica con dominio."""
    flat = []
    for domain, info in sorted(relations_data.items()):
        for rel in info["relations"]:
            flat.append(
                {
                    "domain": domain,
                    "from": rel.get("from"),
                    "via": rel.get("via"),
                    "to": rel.get("to"),
                    "as": rel.get("as", rel.get("via")),
                    "cardinality": rel.get("cardinality", "?"),
                    "key_type": rel.get("key_type", "domain"),
                    "validated_match": rel.get("validated_match"),
                    "validated_on": rel.get("validated_on"),
                    "note": rel.get("note", ""),
                }
            )
    return flat


def build() -> dict[str, Any]:
    """Genera il relationship map completo: territoriale + cross-dominio."""
    data = _load_join_map()
    relations_data = _load_relations_files()

    registries = _build_registry_keys(data)
    unconnected = _find_unconnected(data)
    cross_relations = _build_cross_relations(relations_data)

    # Riepilogo per dominio
    by_domain = {}
    for cr in cross_relations:
        d = cr["domain"]
        if d not in by_domain:
            by_domain[d] = 0
        by_domain[d] += 1

    return {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": "Mappa delle relazioni tra dataset clean del DataCivicLab.",
        "hub_hint": "Usa 'registries' per relazioni territoriali (hub→comuni_master). Usa 'cross_relations' per relazioni cross-dataset per dominio.",
        "registries": registries,
        "unconnected_datasets": unconnected,
        "cross_relations": cross_relations,
        "cross_relations_summary": by_domain,
    }
