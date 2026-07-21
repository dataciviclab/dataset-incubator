-- ISPRA Emissioni GHG per settore economico
-- Fonte: Tabella 1 - Emissioni di gas serra da processi energetici per settore
-- Unità: Mt CO2 equivalente
-- Periodo: 1990-2023

SELECT
    cast_int("anno") AS anno,
    cast_double("industrie_energetiche") AS industrie_energetiche,
    cast_double("industrie_manifatturiere") AS industrie_manifatturiere,
    cast_double("residenziale_e_servizi") AS residenziale_e_servizi,
    cast_double("trasporti") AS trasporti,
    cast_double("totale") AS totale
FROM raw_input
WHERE cast_int("anno") IS NOT NULL
ORDER BY anno
