"""Costruisce la mappa invertita delle relazioni tra dataset dalla join_map.yaml.

Legge la join_map e produce una mappa inversa: per ogni chiave
(codice_istat, denominazione, ...) elenca tutti i dataset che
la condividono, con il normalizzatore e la granularità.

Usata da dataset_graph() per navigare le relazioni live.

Uso::

    from clean_query_mcp.build_relationship_map import build
    mappa = build()
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

DI_ROOT = Path(__file__).resolve().parents[2]
JOIN_MAP_PATH = DI_ROOT / "registry" / "join_map.yaml"


def _load_join_map() -> dict[str, Any]:
    with open(JOIN_MAP_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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


def build() -> dict[str, Any]:
    """Genera il relationship map completo."""
    data = _load_join_map()
    registries = _build_registry_keys(data)
    unconnected = _find_unconnected(data)

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": "Mappa delle relazioni tra dataset clean del DataCivicLab.",
        "hub_hint": "comuni_master e' il golden record centrale. Ogni dataset si collega tramite una delle sue chiavi.",
        "registries": registries,
        "unconnected_datasets": unconnected,
    }
