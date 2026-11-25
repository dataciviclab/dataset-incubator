-- API DGSAIE weekly type=ALL: valori in millesimi di euro (es. 1115,75 => 1,11575 €/L).

SELECT
    TRY_CAST(DATA_RILEVAZIONE AS DATE) AS data_rilevazione,
    CAST(CODICE_PRODOTTO AS VARCHAR) AS codice_prodotto,
    normalize_string(NOME_PRODOTTO) AS prodotto,
    TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE) / 1000.0 AS prezzo_eur,
    TRY_CAST(normalize_italian_number(ACCISA) AS DOUBLE) / 1000.0 AS accisa_eur,
    TRY_CAST(normalize_italian_number(IVA) AS DOUBLE) / 1000.0 AS iva_eur,
    TRY_CAST(normalize_italian_number(NETTO) AS DOUBLE) / 1000.0 AS netto_eur,
    TRY_CAST(normalize_italian_number(VARIAZIONE) AS DOUBLE) / 1000.0 AS variazione_eur,
    CASE
        WHEN TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE) > 0
        THEN 100.0 * TRY_CAST(normalize_italian_number(ACCISA) AS DOUBLE)
             / TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE)
        ELSE NULL
    END AS quota_accisa_pct
FROM raw_input
WHERE DATA_RILEVAZIONE IS NOT NULL
  AND TRIM(DATA_RILEVAZIONE) <> ''
  AND CODICE_PRODOTTO IS NOT NULL
  AND TRIM(PREZZO) <> ''
