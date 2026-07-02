"""Test per build_relationship_map.py — genera mappa relazioni da join_map.yaml.

Legge join_map.yaml committed nel repo e verifica che la mappa generata
abbia la struttura attesa. Usata da dataset_graph() per navigazione live.
"""

from __future__ import annotations

import pytest

from tools.clean_query_mcp import build_relationship_map

pytestmark = pytest.mark.pure_unit


class TestBuildRelationshipMap:
    """Verifica che la generazione della relationship map sia corretta."""

    def test_build_returns_dict(self):
        """build() deve restituire un dict con la struttura attesa."""
        result = build_relationship_map.build()
        assert isinstance(result, dict)
        assert "schema_version" in result
        assert "generated_at" in result
        assert "registries" in result
        assert "unconnected_datasets" in result

    def test_registries_contain_comuni_master(self):
        """Il registro comuni_master deve essere presente con le chiavi attese."""
        result = build_relationship_map.build()
        regs = result["registries"]
        assert "comuni_master" in regs
        keys = regs["comuni_master"]["keys"]
        # Deve avere almeno le 3 chiavi principali
        expected_keys = {"codice_istat", "codice_catastale", "denominazione"}
        assert expected_keys.issubset(keys.keys())

    def test_codice_istat_has_population(self):
        """codice_istat deve contenere popolazione tra i suoi dataset."""
        result = build_relationship_map.build()
        keys = result["registries"]["comuni_master"]["keys"]
        istat_slugs = {d["slug"] for d in keys["codice_istat"]["datasets"]}
        assert "popolazione_istat_comunale_2019_2025" in istat_slugs
        assert "irpef_comunale" in istat_slugs

    def test_codice_catastale_has_rdc(self):
        """codice_catastale deve contenere RdC/PdC."""
        result = build_relationship_map.build()
        keys = result["registries"]["comuni_master"]["keys"]
        cat_slugs = {d["slug"] for d in keys["codice_catastale"]["datasets"]}
        assert "inps_rdc_pdc" in cat_slugs

    def test_denominazione_has_text_datasets(self):
        """denominazione deve contenere i dataset joinati per testo."""
        result = build_relationship_map.build()
        keys = result["registries"]["comuni_master"]["keys"]
        denom_slugs = {d["slug"] for d in keys["denominazione"]["datasets"]}
        assert "opencivitas_fsc_2025_rso" in denom_slugs
        assert "mim_anagrafica_scuole_statali" in denom_slugs
        assert "dipendenti_pubblici" in denom_slugs

    def test_unconnected_datasets_is_list(self):
        """unconnected_datasets deve essere una lista."""
        result = build_relationship_map.build()
        assert isinstance(result["unconnected_datasets"], list)
        assert len(result["unconnected_datasets"]) > 0
        # Deve contenere dataset regionali/nazionali
        slugs = {d["slug"] for d in result["unconnected_datasets"]}
        assert "aifa_spesa_consumo" in slugs
        assert "istat_gini_regionale" in slugs

    def test_dataset_has_required_fields(self):
        """Ogni dataset collegato deve avere slug e normalizer."""
        result = build_relationship_map.build()
        for reg in result["registries"].values():
            for key in reg["keys"].values():
                for ds in key["datasets"]:
                    assert "slug" in ds, f"Dataset senza slug: {ds}"
                    assert "via" in ds
                    assert "normalizer" in ds

    def test_bridge_bdap_registry(self):
        """bdap_anagrafe_enti deve essere presente con bridge_keys."""
        result = build_relationship_map.build()
        assert "bdap_anagrafe_enti" in result["registries"]
        bridge = result["registries"]["bdap_anagrafe_enti"]
        assert "bridge_keys" in bridge
        assert len(bridge["bridge_keys"]) >= 4
