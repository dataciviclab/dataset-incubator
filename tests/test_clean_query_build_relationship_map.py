"""Test per entity_graph.json — grafo entità generato da clean_catalog.json.

Verifica che il grafo abbia la struttura attesa e contenga le entità
e i bridge fondamentali per il Lab.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.pure_unit

GRAPH_PATH = Path(__file__).resolve().parents[1] / "registry" / "entity_graph.json"


def _load() -> dict:
    if not GRAPH_PATH.exists():
        pytest.skip("entity_graph.json non trovato. Esegui: python tools/graph/build_graph.py")
    return json.loads(GRAPH_PATH.read_text())


class TestEntityGraph:
    """Verifica che il grafo entità sia corretto."""

    def test_graph_has_entities(self):
        """Il grafo deve avere entità con dataset collegati."""
        graph = _load()
        assert "entities" in graph
        assert len(graph["entities"]) >= 10  # almeno 10 entità

    def test_entity_comune_has_datasets(self):
        """L'entità Comune deve avere dataset collegati."""
        graph = _load()
        entities = graph["entities"]
        comune = entities.get("Comune") or entities.get("Comune (ISTAT)")
        assert comune is not None, "Entità Comune non trovata"
        assert len(comune["datasets"]) > 10, "Troppi pochi dataset per Comune"

        slugs = {d["slug"] for d in comune["datasets"]}
        assert "popolazione_istat_comunale_2019_2025" in slugs
        assert "irpef_comunale" in slugs

    def test_entity_provincia_has_datasets(self):
        """L'entità Provincia deve avere dataset."""
        graph = _load()
        entities = graph["entities"]
        prov = entities.get("Provincia")
        assert prov is not None
        assert len(prov["datasets"]) > 10

    def test_bridges_present(self):
        """Devono esserci bridge CIG, BDAP, CUP."""
        graph = _load()
        bridges = graph.get("bridges", [])
        assert len(bridges) > 10  # almeno 10 bridge

        # Verifica bridge CIG
        cig_bridges = [b for b in bridges if "cig" in str(b).lower()]
        assert len(cig_bridges) > 0, "Nessun bridge CIG trovato"

        # Verifica bridge BDAP
        bdap_bridges = [b for b in bridges if "bdap" in str(b).lower()]
        assert len(bdap_bridges) > 0, "Nessun bridge BDAP trovato"

    def test_bridges_have_on_column(self):
        """Ogni bridge deve dichiarare la colonna di join (`to.on`).

        Regressione: la chiave YAML `on:` veniva parsificata come booleano
        True da YAML 1.1, quindi `bridge.get("on", "")` restituiva sempre ""
        e il grafo perdeva la colonna di join (CIG, CUP, ...).
        """
        graph = _load()
        bridges = graph.get("bridges", [])
        assert bridges, "Nessun bridge da verificare"
        empty_on = [b for b in bridges if not b.get("to", {}).get("on")]
        assert not empty_on, (
            f"{len(empty_on)} bridge con colonna di join vuota: "
            f"{[b['from']['dataset'] for b in empty_on[:5]]}"
        )

    def test_bridges_no_duplicates(self):
        """Non devono esistere relazioni duplicate (stesso dataset → stesso bridge).

        Regressione: il builder generava una relazione per ogni colonna con
        lo stesso semantic_type (es. anac_bandi_gara con 3 colonne cig_code
        produceva 3 bridge identici).
        """
        graph = _load()
        bridges = graph.get("bridges", [])
        seen = set()
        dups = []
        for b in bridges:
            key = (
                b["from"]["entity"],
                b["from"]["dataset"],
                b["from"]["via"],
                b["to"]["entity"],
                b["to"]["bridge"],
                b["to"]["semantic_type"],
            )
            if key in seen:
                dups.append(key)
            seen.add(key)
        assert not dups, f"{len(dups)} relazioni duplicate trovate: {dups[:5]}"

    def test_entity_has_required_fields(self):
        """Ogni dataset in un'entità deve avere slug, column, semantic_type."""
        graph = _load()
        for entity, info in graph["entities"].items():
            for ds in info["datasets"]:
                assert "slug" in ds, f"{entity}: dataset senza slug"
                assert "column" in ds, f"{entity}: {ds.get('slug')} senza column"
                assert "semantic_type" in ds, f"{entity}: {ds.get('slug')} senza semantic_type"

    def test_summary(self):
        """Il grafo deve avere un summary con total_entities e total_relations."""
        graph = _load()
        assert "summary" in graph
        assert graph["summary"]["total_entities"] >= 10
