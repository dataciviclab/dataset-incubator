"""Tests per _assign_semantic_type e _load_semantic_type_map.

Contratto: l'assegnazione del tipo semantico avviene SOLO per match esatto
sul nome colonna (case-insensitive). Niente substring/partial match.

Prova del fuoco: se qualcuno riaggiunge partial match, colonne come
``comune_litoraneo`` o ``comune_abitanti`` verrebbero erroneamente
classificate come ``municipality_name``. Questo test lo blocca.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.pure_unit

SEMTYPES_PATH = Path(__file__).resolve().parents[1] / "registry" / "semantic_types.yaml"


@pytest.fixture
def alias_map():
    """Carica la mappa alias dal file YAML (reale, non mock)."""
    from scripts.build_clean_catalog import _load_semantic_type_map

    return _load_semantic_type_map()


class TestLoadSemanticTypeMap:
    """Verifica che _load_semantic_type_map carichi correttamente."""

    def test_returns_dict(self, alias_map):
        """Deve restituire un dict (non piu' una tupla)."""
        assert isinstance(alias_map, dict)
        assert len(alias_map) > 20  # almeno 20 alias noti

    def test_key_is_lowercase(self, alias_map):
        """Tutte le chiavi devono essere lowercase."""
        for k in alias_map:
            assert k == k.lower(), f"Alias non lowercase: {k}"

    def test_contains_critical_aliases(self, alias_map):
        """Alias critici devono essere presenti."""
        assert alias_map.get("cig") == "cig_code"
        assert alias_map.get("codice_istat") == "municipality_code"
        assert alias_map.get("codice_fiscale") == "fiscal_code"
        assert alias_map.get("codice_ipa") == "ipa_code"

    def test_file_not_found_returns_empty(self):
        """Se semantic_types.yaml non esiste, ritorna dict vuoto."""
        from scripts.build_clean_catalog import _load_semantic_type_map

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "scripts.build_clean_catalog.SEMTYPES_PATH",
                Path("/tmp/non_existent.yaml"),
            )
            result = _load_semantic_type_map()
            assert result == {}


class TestAssignSemanticType:
    """Verifica che _assign_semantic_type usi solo match esatto."""

    def test_exact_match(self, alias_map):
        """Colonna che matcha esattamente un alias deve essere riconosciuta."""
        from scripts.build_clean_catalog import _assign_semantic_type

        assert _assign_semantic_type("cig", alias_map) == "cig_code"
        assert _assign_semantic_type("codice_istat", alias_map) == "municipality_code"
        assert _assign_semantic_type("comune", alias_map) == "municipality_name"
        assert _assign_semantic_type("provincia", alias_map) == "province_code"
        assert _assign_semantic_type("regione", alias_map) == "region_code"

    def test_case_insensitive(self, alias_map):
        """Il match deve essere case-insensitive."""
        from scripts.build_clean_catalog import _assign_semantic_type

        assert _assign_semantic_type("CIG", alias_map) == "cig_code"
        assert _assign_semantic_type("Codice_Istat", alias_map) == "municipality_code"
        assert _assign_semantic_type("COMUNE", alias_map) == "municipality_name"

    @pytest.mark.parametrize(
        "col_name",
        [
            # BOOLEAN con substring "comune" — NON deve matchare
            "comune_litoraneo",
            "comune_isolano",
            "comune_costiero",
            "flag_comune",
            # Metriche/ID con substring "comune" — NON deve matchare
            "comune_abitanti",
            "comune_id",
            "comune_popolazione",
            # Nomi enti — NON deve matchare
            "denominazione_ente",
            "denominazione_scuola",
            "denominazione_impresa",
            # Descrizioni ATECO — NON deve matchare
            "descr_codice_ateco",
            "descrizione_ateco",
            # Date — NON deve matchare come year
            "data_elezione",
            "data_pubblicazione",
            "data_delibera",
        ],
    )
    def test_no_partial_match(self, alias_map, col_name):
        """Substring NON deve matchare — solo match esatto sull'intero nome."""
        from scripts.build_clean_catalog import _assign_semantic_type

        result = _assign_semantic_type(col_name, alias_map)
        assert result is None, (
            f"ERRORE: '{col_name}' ha ricevuto semantic_type='{result}'. "
            f"Dovrebbe essere None (nessun match esatto)."
        )

    def test_exact_match_for_alias_in_list(self, alias_map):
        """Alias nella lista devono matchare esattamente (non solo i primi)."""
        from scripts.build_clean_catalog import _assign_semantic_type

        # CIG_PROG_ESTERNA e CIG_COLLEGAMENTO sono alias noti di cig_code
        assert _assign_semantic_type("CIG_PROG_ESTERNA", alias_map) == "cig_code"
        assert _assign_semantic_type("CIG_COLLEGAMENTO", alias_map) == "cig_code"
        # cod_cpv_principale e' alias di cpv_code
        assert _assign_semantic_type("cod_cpv_principale", alias_map) == "cpv_code"

    def test_unknown_column_returns_none(self, alias_map):
        """Colonne senza nessun alias devono restituire None."""
        from scripts.build_clean_catalog import _assign_semantic_type

        assert _assign_semantic_type("random_colonna_123", alias_map) is None
        assert _assign_semantic_type("abcdef", alias_map) is None
        assert _assign_semantic_type("x", alias_map) is None

    def test_cig_variants_exact_only(self, alias_map):
        """Varianti CIG devono matchare solo per alias esatti."""
        from scripts.build_clean_catalog import _assign_semantic_type

        # Match esatti
        assert _assign_semantic_type("cig", alias_map) == "cig_code"
        assert _assign_semantic_type("codice_cig", alias_map) == "cig_code"

        # Non match (substring)
        assert _assign_semantic_type("cig_qualcosa", alias_map) is None


class TestEnrichTagsAndCategory:
    """Contratto: _enrich_tags_and_category popola tags nel catalogo dai dataset.yml."""

    def test_tags_populated_from_candidate(self, tmp_path):
        from scripts.build_clean_catalog import _enrich_tags_and_category

        (tmp_path / "candidates" / "demo").mkdir(parents=True)
        yml = tmp_path / "candidates" / "demo" / "dataset.yml"
        yml.write_text(
            "dataset:\n  name: demo\n  years: [2024]\n  tags: [energia]\n", encoding="utf-8"
        )
        catalog = {"datasets": [{"slug": "demo"}]}
        _enrich_tags_and_category(catalog, tmp_path)
        assert catalog["datasets"][0]["tags"] == ["energia"]
