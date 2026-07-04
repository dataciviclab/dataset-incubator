-- clean.sql - terna_electrical_energy_by_sector
-- Input: workbook XLSX (gia' pulito dal footer "Applied filters" da scripts/fetch_terna.py)
-- Colonne: Anno, Regione, Provincia, Settore, Consumo (GWh)
-- Obiettivo: normalizzare colonne e tipi

SELECT
    CAST("Anno" AS INTEGER) AS anno,
    TRIM(CAST("Regione" AS VARCHAR)) AS regione,
    TRIM(CAST("Provincia" AS VARCHAR)) AS provincia,
    TRIM(CAST("Settore" AS VARCHAR)) AS settore,
    ROUND(CAST("Consumo (GWh)" AS DOUBLE), 3) AS consumo_gwh
FROM raw_input
WHERE TRY_CAST("Anno" AS INTEGER) IS NOT NULL
  AND TRIM(CAST("Settore" AS VARCHAR)) <> ''
  AND CAST("Consumo (GWh)" AS DOUBLE) >= 0
