-- clean.sql — malasanita_a_strutture_asl
-- Input:  strutture_asl_2022.csv (granularità: ASL)
-- Output: una riga per ASL, colonne rinominate snake_case, anno = {{year}}
-- Nota:   DuckDB trimma automaticamente i nomi colonna (es. "Regione " → "Regione")

SELECT
    CAST("Anno di Riferimento" AS INTEGER)             AS anno,
    TRIM(CAST("Codice Regione" AS VARCHAR))            AS codice_regione,
    TRIM("Regione")                                    AS regione,
    CAST("Codice Azienda Sanitaria Locale" AS INTEGER) AS codice_asl,
    TRIM("Denominazione ASL")                          AS denominazione_asl,
    CAST("Totale medici" AS INTEGER)                   AS totale_medici,
    CAST("Totale pediatri" AS INTEGER)                 AS totale_pediatri,
    CAST("Totale Residenti" AS BIGINT)                 AS totale_residenti

FROM raw_input
WHERE CAST("Anno di Riferimento" AS INTEGER) = {year}
