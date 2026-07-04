-- clean.sql - terna_electrical_energy_by_sector
-- Input: workbook XLSX (gia' pulito dal footer "Applied filters" da scripts/fetch_terna.py)
-- Colonne: Anno, Regione, Provincia, Settore, Consumo (GWh)
-- Obiettivo: normalizzare colonne e tipi, aggregare per provincia/settore
-- (2015-2020 hanno dati disaggregati, 2021-2024 gia' aggregati)

SELECT
    CAST("Anno" AS INTEGER) AS anno,
    TRIM(CAST("Regione" AS VARCHAR)) AS regione,
    TRIM(CAST("Provincia" AS VARCHAR)) AS provincia,
    TRIM(CAST("Settore" AS VARCHAR)) AS settore,
    ROUND(SUM(CAST("Consumo (GWh)" AS DOUBLE)), 3) AS consumo_gwh
FROM raw_input
WHERE TRY_CAST("Anno" AS INTEGER) IS NOT NULL
  AND TRIM(CAST("Settore" AS VARCHAR)) <> ''
  AND CAST("Consumo (GWh)" AS DOUBLE) >= 0
GROUP BY 1, 2, 3, 4
ORDER BY 1 DESC, 2, 3, 4
