"""
_key_synonyms.py — Vocabolario unico delle chiavi di join riconoscibili.

Questo file è la SINGLE SOURCE OF TRUTH per tutti gli script che devono
riconoscere colonne di join per nome (detection, discovery, scanning).

Usato da:
  - discover_relations.py  (scopre relazioni su parquet reali)
  - joinability_scan.py    (scanner su dati SO, detection per nome)
  - validate_relations.py  (validatore, per normalizzazione nomi)

Regole:
  - KEY_SYNONYMS: mapping famiglia_di_chiave → lista di nomi colonna
  - KEY_WEIGHTS: peso (0-100) per calcolare qualità della detection
  - SKIP_FAMILIES: famiglie troppo generiche da escludere dai lead
  - CHIAVE_TERRITORIALI / CHIAVE_DOMINIO / CHIAVE_ANAGRAFICHE: raggruppamenti
"""

# ── KEY SYNONYMS ─────────────────────────────────────────────────────────
# Ogni entry: "famiglia" → lista di nomi colonna (esatti o comunemente usati)
# che rappresentano quella chiave nel dataset.

KEY_SYNONYMS: dict[str, list[str]] = {
    # ── TERRITORIO ────────────────────────────────────────────────────────
    "codice_istat": [
        "codice_istat",
        "codice_istat_comune",
        "codice_istat_luogo",
        "codice_comune",
        "cod_comune",
        "pro_com",
        "codice_comune_istat",
        "codice_comune_comune",
        "localizzazione_codice_istat",
        "luogo_istat",
        "codice_istat_ipa",
        "comune_istat",
        "cod_istat_comune",
        "comune_codice",
        "cod_comune_istat",
    ],
    "codice_catastale": [
        "codice_catastale",
        "cod_catastale",
        "catastale",
        "codice_belfiore",
    ],
    "regione": [
        "regione",
        "codice_regione",
        "cod_regione",
        "cod_reg",
        "regione_codice",
        "istat_regione",
    ],
    "provincia": [
        "provincia",
        "sigla_provincia",
        "codice_provincia",
        "sigla_prov",
        "cod_prov",
        "prov",
    ],
    "comune_nome": [
        "comune",
        "denominazione_comune",
        "comune_descrizione",
        "comune_denominazione",
    ],
    # ── DOMINIO APPALTI ──────────────────────────────────────────────────
    "cig": [
        "cig",
        "codice_cig",
        "cig_accordo_quadro",
        "CIG_PROG_ESTERNA",
        "CIG_COLLEGAMENTO",
    ],
    "id_aggiudicazione": [
        "id_aggiudicazione",
        "id_aggiudicazione",
    ],
    "cod_cpv": [
        "cod_cpv",
        "codice_cpv",
        "cpv",
        "cod_cpv_principale",
    ],
    "codice_ausa": [
        "codice_ausa",
        "ausa",
    ],
    "cui": [
        "cui",
        "cui_programma",
        "codice_cui",
    ],
    # ── DOMINIO GIUSTIZIA ────────────────────────────────────────────────
    "numero_ricorso": [
        "numero_ricorso",
        "NUMERO_RICORSO",
        "NUMERO_PROVVEDIMENTO",
        "n_ricorso",
    ],
    # ── ANAGRAFICA ENTI ──────────────────────────────────────────────────
    "partita_iva": [
        "partita_iva",
        "p_iva",
        "piva",
        "codice_fiscale",
        "codice_fiscale_ente",
        "cf",
        "cf_amministrazione_appaltante",
        "cf_soggetto_attuatore",
        "cf_subappaltante",
        "CF_SA_DELEGANTE",
        "CF_SA_DELEGATA",
        "codice_fiscale_ente",
    ],
    "codice_ipa": [
        "codice_ipa",
        "ipa",
        "cod_ipa",
    ],
    # ── DOMINIO SCUOLA ───────────────────────────────────────────────────
    "codice_scuola": [
        "codice_scuola",
        "codicescuola",
        "codice_meccanografico",
        "cod_scuola",
    ],
    # ── CLASSIFICAZIONI ──────────────────────────────────────────────────
    "ateco": [
        "ateco",
        "codice_ateco",
        "sezione_ateco",
        "ateco_code",
    ],
    "nazione": [
        "nazione",
        "stato",
        "paese",
        "country",
        "codice_nazione",
    ],
    # ── CLASSIFICAZIONI EUROPEE ──────────────────────────────────────────
    "nuts": [
        "nuts",
        "codice_nuts",
        "nuts2",
        "nuts3",
        "nuts_code",
    ],
}

# ── PESI PER QUALITÀ DETECTION ──────────────────────────────────────────
# Usati da joinability_scan.py per calcolare quality_score.
# Peso più alto = chiave più distintiva e utile.

KEY_WEIGHTS: dict[str, int] = {
    # Territoriali (molto informative)
    "codice_istat": 20,
    "codice_catastale": 15,
    # Appalti
    "cig": 25,
    "id_aggiudicazione": 25,
    "cod_cpv": 10,
    "codice_ausa": 15,
    "cui": 15,
    # Giustizia
    "numero_ricorso": 20,
    # Enti
    "partita_iva": 15,
    "codice_ipa": 15,
    # Scuola
    "codice_scuola": 15,
    # Classificazioni
    "ateco": 8,
    "nuts": 8,
    # Generiche (peso basso)
    "regione": 5,
    "provincia": 5,
    "comune_nome": 3,
    "nazione": 3,
}

# ── FAMIGLIE DA SALTARE NEI LEAD ────────────────────────────────────────
# Queste famiglie sono troppo generiche per generare lead di intake
# (es. "provincia" da sola non basta per dire che una fonte è joinabile).

SKIP_FAMILIES: set[str] = {"provincia", "regione", "nazione", "comune_nome"}

# ── RAGGRUPPAMENTI ──────────────────────────────────────────────────────
# Per navigazione e categorizzazione.

CHIAVE_TERRITORIALI: set[str] = {
    "codice_istat",
    "codice_catastale",
    "regione",
    "provincia",
    "comune_nome",
}
CHIAVE_DOMINIO: set[str] = {
    "cig",
    "id_aggiudicazione",
    "cod_cpv",
    "codice_ausa",
    "cui",
    "numero_ricorso",
}
CHIAVE_ANAGRAFICHE: set[str] = {
    "partita_iva",
    "codice_ipa",
    "codice_scuola",
}
CHIAVE_CLASSIFICAZIONI: set[str] = {
    "ateco",
    "nuts",
    "nazione",
}
