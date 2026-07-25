-- Clean: comuni_master
-- Fusione di:
--   istat-elenco-comuni (ISTAT SITUAS, da GCS): dati territoriali, popolazione
--   ISTAT CSV (da URL): codici NUTS, ripartizione, flag capoluogo, codici storici
--   ipa-enti (AgID IPA, da GCS): codici IPA, fiscale, contatti
-- Una riga per comune italiano con tutte le codifiche.
-- La chiave tra istat-elenco-comuni e ISTAT CSV è il codice ISTAT.
-- La chiave con IPA è il codice catastale (Belfiore): universale e presente in
-- entrambe le fonti (il codice ISTAT in IPA non coincide per tutte le regioni,
-- es. Sardegna).

WITH

-- Hub: dati territoriali da istat-elenco-comuni (SITUAS)
hub AS (
    SELECT * FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/istat_elenco_comuni/2026/istat_elenco_comuni_2026_clean.parquet',
        union_by_name=true
    )
),

-- ISTAT CSV: codici NUTS 2021/2024, ripartizione, flag capoluogo, tipologia UTS,
-- denominazione multilingue, codici storici per mapping tra sistemi provinciali
istat_nuts AS (
    SELECT
        lpad(trim(col_cod_istat), 6, '0') AS codice_istat,
        upper(trim(col_cod_catastale)) AS codice_catastale,
        trim(col_nuts1_2021) AS nuts1_2021,
        trim(col_nuts2_2021) AS nuts2_2021,
        trim(col_nuts3_2021) AS nuts3_2021,
        trim(col_nuts1_2024) AS nuts1_2024,
        trim(col_nuts2_2024) AS nuts2_2024,
        trim(col_nuts3_2024) AS nuts3_2024,
        try_cast(col_cod_ripartizione AS INTEGER) AS codice_ripartizione,
        trim(col_ripartizione) AS ripartizione,
        CASE WHEN trim(col_flag_capoluogo) = '1' THEN TRUE ELSE FALSE END AS flag_capoluogo,
        try_cast(col_tipologia_uts AS INTEGER) AS codice_tipologia_uts,
        trim(col_denominazione_uts) AS denominazione_uts,
        nullif(trim(col_denominazione_altra), '') AS denominazione_altra_lingua,
        lpad(trim(col_cod_110province), 6, '0') AS codice_110_province,
        lpad(trim(col_cod_107province), 6, '0') AS codice_107_province,
        lpad(trim(col_cod_103province), 6, '0') AS codice_103_province
    FROM read_csv(
        '{root}/data/raw/{dataset}/{year}/istat_codici.csv',
        delim=';', header=false, skip=3,
        strict_mode=false, ignore_errors=true, all_varchar=true,
        quote='"', escape='"', max_line_size=500000,
        columns = {
            'col_cod_regione': 'VARCHAR', 'col_uts': 'VARCHAR',
            'col_cod_provincia': 'VARCHAR', 'col_progressivo': 'VARCHAR',
            'col_cod_alfanumerico': 'VARCHAR', 'col_denominazione_en': 'VARCHAR',
            'col_denominazione': 'VARCHAR', 'col_denominazione_altra': 'VARCHAR',
            'col_cod_ripartizione': 'VARCHAR', 'col_ripartizione': 'VARCHAR',
            'col_denominazione_regione': 'VARCHAR', 'col_denominazione_uts': 'VARCHAR',
            'col_tipologia_uts': 'VARCHAR', 'col_flag_capoluogo': 'VARCHAR',
            'col_sigla_provincia': 'VARCHAR', 'col_cod_istat': 'VARCHAR',
            'col_cod_110province': 'VARCHAR', 'col_cod_107province': 'VARCHAR',
            'col_cod_103province': 'VARCHAR', 'col_cod_catastale': 'VARCHAR',
            'col_nuts1_2021': 'VARCHAR', 'col_nuts2_2021': 'VARCHAR',
            'col_nuts3_2021': 'VARCHAR', 'col_nuts1_2024': 'VARCHAR',
            'col_nuts2_2024': 'VARCHAR', 'col_nuts3_2024': 'VARCHAR'
        }
    )
    WHERE col_cod_istat IS NOT NULL AND trim(col_cod_istat) != ''
),

-- IPA enti (da GCS): solo categoria L6 (Comuni)
-- Raggruppa per codice catastale per prendere il miglior match
ipa AS (
    SELECT
        trim(codice_catastale_comune) AS cod_cat,
        any_value(codice_ipa ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS codice_ipa,
        any_value(codice_fiscale_ente ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS codice_fiscale,
        any_value(denominazione_ente ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS denominazione_ipa,
        any_value(codice_categoria ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS codice_categoria,
        any_value(trim(codice_catastale_comune) ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS codice_catastale_comune,
        any_value(codice_istat ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS codice_istat_ipa,
        any_value(acronimo ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS acronimo,
        any_value(indirizzo ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS indirizzo,
        any_value(cap ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS cap,
        any_value(sito_istituzionale ORDER BY CASE WHEN lower(codice_ipa) LIKE 'c\_%' ESCAPE '\' THEN 0 ELSE 1 END, codice_ipa) AS sito_istituzionale
    FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/ipa_enti/2026/ipa_enti_2026_clean.parquet',
        union_by_name=true
    )
    WHERE codice_categoria = 'L6'
      AND codice_catastale_comune IS NOT NULL AND trim(codice_catastale_comune) != ''
    GROUP BY codice_catastale_comune
)

SELECT
    -- Chiave
    h.codice_istat,

    -- Anagrafica comune (da hub)
    h.denominazione,
    h.codice_catastale,
    h.sigla_provincia,
    h.provincia,
    h.regione,

    -- Dati territoriali (da hub)
    h.superficie_km2,
    h.popolazione_residente,
    h.popolazione_legale,
    h.zona_altimetrica,
    h.altitudine,
    h.comune_litoraneo,
    h.comune_isolano,

    -- NUTS (da ISTAT CSV)
    n.nuts1_2021, n.nuts2_2021, n.nuts3_2021,
    n.nuts1_2024, n.nuts2_2024, n.nuts3_2024,

    -- Ripartizione geografica
    n.codice_ripartizione, n.ripartizione, n.flag_capoluogo,
    n.codice_tipologia_uts, n.denominazione_uts,
    n.denominazione_altra_lingua,

    -- Codici storici
    n.codice_110_province, n.codice_107_province, n.codice_103_province,

    -- Codici IPA (da ipa-enti)
    ip.codice_ipa, ip.codice_fiscale, ip.denominazione_ipa,
    ip.codice_categoria, ip.codice_catastale_comune, ip.codice_istat_ipa,
    ip.acronimo,

    -- Contatti (da ipa-enti)
    ip.indirizzo, ip.cap, ip.sito_istituzionale

FROM hub h
LEFT JOIN istat_nuts n ON upper(trim(h.codice_catastale)) = n.codice_catastale
LEFT JOIN ipa ip ON upper(trim(h.codice_catastale)) = upper(trim(ip.cod_cat))
ORDER BY h.codice_istat
