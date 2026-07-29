"""Carica il grafo entità da entity_graph.json (generato da build_graph.py).

Legge:
  - registry/entity_graph.json   → grafo entità → dataset (generato automaticamente)

Usata da dataset_graph() nel MCP server.

Niente più YAML manuali: il grafo viene generato da build_graph.py che
legge clean_catalog.json (con semantic_type) + semantic_types.yaml.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DI_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = DI_ROOT / "registry" / "entity_graph.json"


def build() -> dict[str, Any]:
    """Carica e restituisce il grafo entità da entity_graph.json."""
    if not GRAPH_PATH.exists():
        return {"error": "entity_graph.json non trovato. Esegui: python tools/graph/build_graph.py"}

    try:
        graph = json.loads(GRAPH_PATH.read_text())
        return {
            "schema_version": 2,
            "description": "Grafo entità → dataset del DataCivicLab. Generato automaticamente da clean_catalog.json + semantic_types.yaml.",
            **graph,
        }
    except Exception as exc:
        return {"error": f"Errore caricamento entity_graph.json: {exc}"}
