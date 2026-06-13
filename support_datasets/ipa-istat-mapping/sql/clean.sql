-- Clean: ipa_istat_mapping
-- Compone IPA enti (AgID) + ISTAT codici amministrativi
-- Fonti:
--   raw_input: IPA enti (datastore dump, UTF-8, delim=',')
--   istat_comuni.csv: ISTAT codici amm.vi (latin-1, delim=';',
--     header multi-riga con nomi lunghi → lettura posizionale)

WITH

-- Legge ISTAT con colonne posizionali (header multi-riga non rilevabile automaticamente)
istat_raw AS (
    SELECT * FROM read_csv(
        '{root}/data/raw/{dataset}/{year}/istat_comuni.csv',
        delim=';',
        header=false,
        skip=1,
        strict_mode=false,
        ignore_errors=true,
        all_varchar=true,
        quote='"',
        escape='"',
        max_line_size=500000,
        columns = {
            'col_cod_regione': 'VARCHAR',
            'col_uts': 'VARCHAR',
            'col_cod_provincia': 'VARCHAR',
            'col_progressivo': 'VARCHAR',
            'col_cod_alfanumerico': 'VARCHAR',
            'col_denominazione_en': 'VARCHAR',
            'col_denominazione': 'VARCHAR',
            'col_denominazione_altra': 'VARCHAR',
            'col_cod_ripartizione': 'VARCHAR',
            'col_ripartizione': 'VARCHAR',
            'col_denominazione_regione': 'VARCHAR',
            'col_denominazione_uts': 'VARCHAR',
            'col_tipologia_uts': 'VARCHAR',
            'col_flag_capoluogo': 'VARCHAR',
            'col_sigla_provincia': 'VARCHAR',
            'col_cod_istat': 'VARCHAR',
            'col_cod_110province': 'VARCHAR',
            'col_cod_107province': 'VARCHAR',
            'col_cod_103province': 'VARCHAR',
            'col_cod_catastale': 'VARCHAR',
            'col_nuts1_2021': 'VARCHAR',
            'col_nuts2_2021': 'VARCHAR',
            'col_nuts3_2021': 'VARCHAR',
            'col_nuts1_2024': 'VARCHAR',
            'col_nuts2_2024': 'VARCHAR',
            'col_nuts3_2024': 'VARCHAR'
        }
    )
),

-- Normalizza ISTAT: pulizia e zero-padding
istat AS (
    SELECT DISTINCT
        lpad(trim(col_cod_istat), 6, '0') AS codice_istat,
        trim(col_denominazione) AS denominazione,
        trim(col_denominazione_regione) AS regione,
        trim(col_sigla_provincia) AS sigla_provincia,
        lpad(trim(col_cod_regione), 2, '0') AS codice_regione,
        trim(col_cod_catastale) AS codice_catastale
    FROM istat_raw
    WHERE col_cod_istat IS NOT NULL
      AND trim(col_cod_istat) != ''
),

-- Filtra IPA: solo enti di categoria Comune (L6)
ipa AS (
    SELECT
        trim(Codice_IPA) AS codice_ipa,
        trim(Denominazione_ente) AS denominazione_ente,
        trim(Codice_fiscale_ente) AS codice_fiscale_ente,
        trim(Codice_Categoria) AS codice_categoria,
        lpad(trim(CAST(Codice_comune_ISTAT AS VARCHAR)), 6, '0')
            AS codice_comune_istat,
        trim(Codice_catastale_comune) AS codice_catastale_comune,
        CAST(Codice_ISTAT AS VARCHAR) AS codice_istat_ipa,
        trim(Acronimo) AS acronimo,
        trim(Indirizzo) AS indirizzo,
        trim(CAP) AS cap,
        trim(Sito_istituzionale) AS sito_istituzionale,
        trim(Mail1) AS mail1,
        trim(Tipo_Mail1) AS tipo_mail1
    FROM raw_input
    WHERE trim(Codice_Categoria) = 'L6'
      AND Codice_comune_ISTAT IS NOT NULL
),

-- LEFT JOIN con dedup: un comune ISTAT può avere zero o più righe IPA
-- Priorità: codice_ipa che inizia con 'c_' (canonico Comune in IPA)
anagrafica_joined AS (
    SELECT
        i.codice_istat,
        i.denominazione,
        i.regione,
        i.sigla_provincia,
        i.codice_regione,
        i.codice_catastale AS codice_catastale_istat,
        ip.codice_ipa,
        ip.codice_fiscale_ente AS codice_fiscale,
        ip.denominazione_ente AS denominazione_ipa,
        ip.codice_categoria,
        ip.codice_catastale_comune,
        ip.codice_istat_ipa,
        ip.acronimo,
        ip.indirizzo,
        ip.cap,
        ip.sito_istituzionale,
        ROW_NUMBER() OVER (
            PARTITION BY i.codice_istat
            ORDER BY
                CASE WHEN ip.codice_ipa LIKE 'c\_%' THEN 0
                     WHEN ip.codice_ipa IS NOT NULL THEN 1
                     ELSE 2 END,
                ip.codice_ipa NULLS LAST
        ) AS rn
    FROM istat i
    LEFT JOIN ipa ip
        ON i.codice_istat = ip.codice_comune_istat
)

-- Output: una riga per comune
SELECT
    codice_istat,
    denominazione,
    regione,
    sigla_provincia,
    codice_regione,
    codice_catastale_istat,
    codice_ipa,
    codice_fiscale,
    denominazione_ipa,
    codice_categoria,
    codice_catastale_comune,
    codice_istat_ipa,
    acronimo,
    indirizzo,
    cap,
    sito_istituzionale
FROM anagrafica_joined
WHERE rn = 1
ORDER BY codice_istat
