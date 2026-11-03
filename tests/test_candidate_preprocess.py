"""Test sui `preprocess.py` dei candidate — parser di layout non tabellari.

I preprocess gestiscono fogli con celle unite, blocchi affiancati, refusi e
cambi di unità: è il codice dove un errore è silenzioso e finisce pubblicato.
Il job `lint` non copre `candidates/`, quindi questi test sono l'unico gate.

Prova del fuoco: senza il test su `ABBRUZZO → ABRUZZO` la serie regionale
dell'Abruzzo si spezza in due senza che nessun gate se ne accorga.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(slug: str) -> ModuleType:
    path = REPO_ROOT / "candidates" / slug / "preprocess.py"
    spec = importlib.util.spec_from_file_location(f"preprocess_{slug.replace('-', '_')}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gas_import() -> ModuleType:
    return _load("mase-gas-import")


@pytest.fixture(scope="module")
def gas_consumi() -> ModuleType:
    return _load("mase-gas-consumi")


@pytest.fixture(scope="module")
def petroliferi() -> ModuleType:
    return _load("mase-consumi-petroliferi")


class TestGasConsumiEtichette:
    """Le etichette regione/provincia cambiano tra gli anni nella fonte."""

    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        ("grezzo", "atteso"),
        [
            ("ABBRUZZO", "ABRUZZO"),  # refuso nella fonte, 11 anni su 22
            ("ABRUZZO", "ABRUZZO"),
            ("  abruzzo ", "ABRUZZO"),
            ("SARDEGNA", "SARDEGNA"),
        ],
    )
    def test_normalize_region(self, gas_consumi: ModuleType, grezzo: str, atteso: str) -> None:
        assert gas_consumi._normalize_region(grezzo) == atteso

    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        ("grezzo", "atteso"),
        [
            ("MONZA-BRIANZA", "MONZA"),  # 2010-2013; dal 2014 la fonte usa MONZA
            ("MONZA", "MONZA"),
        ],
    )
    def test_normalize_province(self, gas_consumi: ModuleType, grezzo: str, atteso: str) -> None:
        assert gas_consumi._normalize_province(grezzo) == atteso

    @pytest.mark.regression
    def test_regioni_attese_e_alias_coerenti(self, gas_consumi: ModuleType) -> None:
        """20 regioni, nessuna variante tra le attese, alias verso regioni valide."""
        assert len(gas_consumi.EXPECTED_REGIONS) == 20
        assert "ABBRUZZO" not in gas_consumi.EXPECTED_REGIONS
        for variante, canonica in gas_consumi.REGION_ALIAS.items():
            assert canonica in gas_consumi.EXPECTED_REGIONS, variante
        for variante, canonica in gas_consumi.PROVINCE_ALIAS.items():
            assert variante != canonica


class TestGasImportEtichette:
    """Le ere usano italiano e inglese, con refusi."""

    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        ("grezzo", "atteso"),
        [
            ("Russian Federation", "RUSSIA"),
            ("Netherlands", "OLANDA"),
            ("QUATAR", "QATAR"),
            ("ALRI UE", "ALTRI UE"),
            ("USA", "U.S.A."),
            ("Trinidad and Tobago", "TRINIDAD"),
            ("AUSTRIA (*)", "AUSTRIA"),
            ("Totale", None),
            ("FONTE: Ministero", None),
            ("", None),
        ],
    )
    def test_normalize_country(
        self, gas_import: ModuleType, grezzo: str, atteso: str | None
    ) -> None:
        assert gas_import._normalize_country(grezzo) == atteso


class TestGasImportSogliaSm3:
    """I file 2013-2014 sono in Sm3 grezzi nonostante il titolo 'Miliardi'."""

    @pytest.mark.regression
    def test_blocco_in_sm3_viene_riscalato(self, gas_import: ModuleType) -> None:
        # Russia gennaio 2013, come nella fonte
        blocco = [(2013, 1, "RUSSIA", 2_462_201_248.0)]
        assert gas_import._scale_block(blocco, "test") == gas_import.RAW_SM3_SCALE

    @pytest.mark.pure_unit
    def test_blocco_in_m_sm3_non_viene_toccato(self, gas_import: ModuleType) -> None:
        blocco = [(2024, 1, "RUSSIA", 700.0), (2024, 1, "ALGERIA", 1499.4)]
        assert gas_import._scale_block(blocco, "test") == 1.0

    @pytest.mark.policy
    def test_soglia_tra_i_due_ordini_di_grandezza(self, gas_import: ModuleType) -> None:
        """Un anno italiano sta sotto 100.000 M Sm3; un blocco in Sm3 sta sopra 1e8."""
        assert 100_000 < gas_import.RAW_SM3_THRESHOLD < 100_000_000


class TestPetroliferiEtichette:
    """Le etichette prodotto variano tra le ere, con marcatori di nota."""

    @pytest.mark.pure_unit
    @pytest.mark.parametrize(
        ("grezzo", "atteso"),
        [
            ("BENZINA(*)", "BENZINA"),
            ("  BENZINA  ", "BENZINA"),
            ("OLIO COMB.LE", "OLIO COMB.LE"),
            ("", None),
            (None, None),
        ],
    )
    def test_clean_label(
        self, petroliferi: ModuleType, grezzo: str | None, atteso: str | None
    ) -> None:
        assert petroliferi._clean_label(grezzo) == atteso

    @pytest.mark.regression
    def test_product_alias_copre_le_varianti(self, petroliferi: ModuleType) -> None:
        for grezzo in ("CARBOT.", "CARBOTURBO"):
            assert petroliferi.PRODUCT_ALIAS[grezzo] == "carboturbo"
        for grezzo in ("OLIO COMB.", "OLIO COMB.LE", "OLIO COMBUSTIBILE"):
            assert petroliferi.PRODUCT_ALIAS[grezzo] == "olio combustibile"
        for grezzo in ("G.P.L.", "GPL"):
            assert petroliferi.PRODUCT_ALIAS[grezzo] == "gpl"
        assert petroliferi.PRODUCT_ALIAS["LUBRIFICANTI TOTALE"] == "lubrificanti"

    @pytest.mark.pure_unit
    def test_varianti_della_riga_totale_allineate(self, petroliferi: ModuleType) -> None:
        for variante in ("TOTALE", "TOTALE (A)", "TOTALE GASOLI", "T O T A L E"):
            assert variante in petroliferi.DETAIL_TOTALE
