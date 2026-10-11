-- API DGSAIE: valori in millesimi di euro.
-- CODICE_MESE 13-17 = Anno/Trimestri aggregati: esclusi dal clean (solo mesi 1-12).

SELECT
    TRY_CAST(ANNO AS INTEGER) AS anno,
    TRY_CAST(CODICE_MESE AS INTEGER) AS mese,
    normalize_string(NOME_MESE) AS nome_mese,
    CAST(CODICE_PRODOTTO AS VARCHAR) AS codice_prodotto,
    normalize_string(NOME_PRODOTTO) AS prodotto,
    TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE) / 1000.0 AS prezzo_eur,
    TRY_CAST(normalize_italian_number(ACCISA) AS DOUBLE) / 1000.0 AS accisa_eur,
    TRY_CAST(normalize_italian_number(IVA) AS DOUBLE) / 1000.0 AS iva_eur,
    TRY_CAST(normalize_italian_number(NETTO) AS DOUBLE) / 1000.0 AS netto_eur,
    CASE
        WHEN TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE) > 0
        THEN 100.0 * TRY_CAST(normalize_italian_number(ACCISA) AS DOUBLE)
             / TRY_CAST(normalize_italian_number(PREZZO) AS DOUBLE)
        ELSE NULL
    END AS quota_accisa_pct
FROM raw_input
WHERE TRY_CAST(ANNO AS INTEGER) IS NOT NULL
  AND TRY_CAST(CODICE_MESE AS INTEGER) BETWEEN 1 AND 12
  AND CODICE_PRODOTTO IS NOT NULL
  AND TRIM(PREZZO) <> ''
