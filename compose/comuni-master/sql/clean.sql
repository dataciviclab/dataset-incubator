-- Clean: comuni_master
-- Fusione di:
--   istat-elenco-comuni (ISTAT SITUAS, da GCS): dati territoriali, popolazione
--   ISTAT CSV (da URL): codici NUTS, ripartizione, flag capoluogo, codici storici
--   ipa-enti (AgID IPA, da GCS): codici IPA, fiscale, contatti
-- Una riga per comune italiano con tutte le codifiche.
-- La chiave con IPA è il codice catastale (Belfiore): universale e presente in
-- entrambe le fonti (il codice ISTAT in IPA non coincide per tutte le regioni,
-- es. Sardegna).
-- Anche la join con l'ISTAT CSV usa il codice catastale (vedi JOIN finale), non
-- il codice ISTAT: la descrizione precedente diceva "codice ISTAT" ed era
-- fuorviante rispetto al codice.
--
-- ENCODING: il CSV ISTAT è CP1252, non UTF-8. Va letto con encoding='cp1252'
-- (vedi read_csv sotto): senza, DuckDB scarta in silenzio le righe con accenti
-- (Agliè, Ciriè, Vallée d'Aoste, toponimi tedeschi del Sudtirolo).

WITH

-- Hub: dati territoriali da istat-elenco-comuni (SITUAS)
hub AS (
    SELECT * FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/istat_elenco_comuni/2026/istat_elenco_comuni_2026_clean.parquet',
        union_by_name=true
    )
),

-- ISTAT CSV: codici NUTS 2021/2024, ripartizione, flag capoluogo, tipologia UTS,
-- denominazione multilingue, codici storici per mapping tra sistemi provinciali.
--
-- ATTENZIONE alla provenienza dei campi: il hub (SITUAS) è fermo alla
-- riorganizzazione provinciale sarda 2005-2016 e usa per la Sardegna codici
-- propri (112-119) con le province abolite (Gallura, Ogliastra, Medio
-- Campidano, Sulcis Iglesiente). L'ISTAT CSV corrente ha 5 province
-- (090/091/092/095/111). Per codice_istat, provincia e sigla vince il CSV,
-- con fallback al hub per le righe non joinate.
istat_nuts AS (
    SELECT
        lpad(trim(col_cod_istat), 6, '0') AS codice_istat,
        upper(trim(col_cod_catastale)) AS codice_catastale,
        trim(col_sigla_provincia) AS sigla_provincia,
        trim(col_denominazione_regione) AS regione,
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
        -- skip=2: l'intestazione ISTAT è UNA riga logica che occupa 3 righe
        -- fisiche (due campi quotati contengono un newline). Con skip=3 si
        -- perdeva la prima riga dati (Agliè): verificato 7.895 vs 7.896 righe.
        delim=';', header=false, skip=2,
        -- encoding: il file ISTAT è CP1252, non UTF-8. Senza questa opzione
        -- DuckDB leggeva come UTF-8 e scartava in silenzio (via
        -- ignore_errors) le 512 righe con accenti: Agliè, Ciriè, Vallée
        -- d'Aoste, i toponimi tedeschi del Sudtirolo.
        encoding='cp1252',
        -- Niente ignore_errors: uno scarto silenzioso qui significa comuni
        -- mancanti nei mart, e il toolkit non può misurarlo (il probe B4
        -- copre solo clean.read). La guardia in load_clean_sql lo rifiuta.
        -- strict_mode=false serve per lo sniffing dell'intestazione multi-linea.
        strict_mode=false, all_varchar=true,
        quote='"', escape='"', max_line_size=500000,
        columns = {
            'col_cod_regione': 'VARCHAR', 'col_uts': 'VARCHAR',
            'col_cod_provincia': 'VARCHAR', 'col_progressivo': 'VARCHAR',
            'col_cod_alfanumerico': 'VARCHAR', 'col_denominazione_en': 'VARCHAR',
            'col_denominazione': 'VARCHAR', 'col_denominazione_altra': 'VARCHAR',
            'col_cod_ripartizione': 'VARCHAR', 'col_ripartizione': 'VARCHAR',
            'col_denominazione_regione': 'VARCHAR', 'col_denominazione_uts': 'VARCHAR',
            'col_tipologia_uts': 'VARCHAR', 'col_flag_capoluogo': 'VARCHAR',
            'col_sigla_provincia': 'VARCHAR', 'col_cod_istat': 'VARCHAR',            'col_cod_110province': 'VARCHAR', 'col_cod_107province': 'VARCHAR',
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
        'https://storage.googleapis.com/dataciviclab-clean/indice-pa/ipa_enti/2026/ipa_enti_2026_clean.parquet',
        union_by_name=true
    )
    WHERE codice_categoria = 'L6'
      AND codice_catastale_comune IS NOT NULL AND trim(codice_catastale_comune) != ''
    GROUP BY codice_catastale_comune
)

SELECT
    -- Chiave: codice ISTAT corrente (CSV), fallback al hub per le righe non
    -- joinate. Il hub è più vecchio per la Sardegna (vedi nota su istat_nuts).
    COALESCE(n.codice_istat, h.codice_istat) AS codice_istat,

    -- Anagrafica comune: denominazione e catastale dal hub (fonte SITUAS),
    -- attribuzione territoriale dall'ISTAT CSV corrente.
    h.denominazione,
    h.codice_catastale,
    COALESCE(n.sigla_provincia, h.sigla_provincia) AS sigla_provincia,
    COALESCE(n.denominazione_uts, h.provincia) AS provincia,
    COALESCE(n.regione, h.regione) AS regione,

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
