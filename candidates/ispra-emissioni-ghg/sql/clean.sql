-- ISPRA Emissioni GHG per settore economico
-- Fonte: Tabella 1 - Emissioni di gas serra da processi energetici per settore
-- Unità: Mt CO2 equivalente
-- Periodo: 1990-2023

SELECT
    TRY_CAST("anno" AS INTEGER) AS anno,
    TRY_CAST("industrie_energetiche" AS DOUBLE) AS industrie_energetiche,
    TRY_CAST("industrie_manifatturiere" AS DOUBLE) AS industrie_manifatturiere,
    TRY_CAST("residenziale_e_servizi" AS DOUBLE) AS residenziale_e_servizi,
    TRY_CAST("trasporti" AS DOUBLE) AS trasporti,
    TRY_CAST("totale" AS DOUBLE) AS totale
FROM raw_input
WHERE TRY_CAST("anno" AS INTEGER) IS NOT NULL
ORDER BY anno
