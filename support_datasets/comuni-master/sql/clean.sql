-- Clean: comuni_master
-- Fusione di istat-elenco-comuni (ISTAT SITUAS) + ipa-istat-mapping (IPA AgID)
-- Fonti:
--   raw_input: istat_clean.parquet (da GCS)
--   {root}/data/raw/{dataset}/{year}/ipa_clean.parquet (da GCS)
-- Una riga per comune italiano con tutte le codifiche e dati territoriali.
-- La chiave di JOIN è il codice catastale (Belfiore), non il codice ISTAT:
-- i codici ISTAT non coincidono tra SITUAS e IPA per tutte le regioni
-- (es. Sardegna: Cagliari 118006 in SITUAS vs 092009 in IPA).

WITH istat AS (
    SELECT * FROM raw_input
),

ipa AS (
    SELECT * FROM read_parquet('{root}/data/raw/{dataset}/{year}/ipa_clean.parquet')
)

SELECT
    -- Chiave
    i.codice_istat,

    -- Anagrafica comune (da ISTAT)
    i.denominazione,
    i.codice_catastale,
    i.sigla_provincia,
    i.provincia,
    i.regione,

    -- Dati territoriali (da ISTAT)
    i.superficie_km2,
    i.popolazione_residente,
    i.popolazione_legale,
    i.zona_altimetrica,
    i.altitudine,
    i.comune_litoraneo,
    i.comune_isolano,

    -- Codici IPA (da IPA)
    ip.codice_ipa,
    ip.codice_fiscale,
    ip.codice_categoria,
    ip.codice_catastale_comune,
    ip.codice_regione,
    ip.codice_istat_ipa,
    ip.denominazione_ipa,
    ip.acronimo,

    -- Contatti (da IPA)
    ip.indirizzo,
    ip.cap,
    ip.sito_istituzionale

FROM istat i
LEFT JOIN ipa ip
    ON upper(trim(i.codice_catastale)) = upper(trim(ip.codice_catastale_istat))
ORDER BY i.codice_istat
