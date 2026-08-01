-- mart_settori_anno — Emissioni GHG per settore x anno (formato long)
--
-- Trasforma il clean wide (1 riga = 1 anno, colonne per settore) in long:
-- 1 riga = 1 settore x anno, con quota % sul totale nazionale.
-- Serve per: ribaltamento quote settoriali (D5), effetto Covid (D6),
-- gap verso obiettivi 2030/2050 (D9), rimbalzo 2022-23 (D10).
--
-- PK: (anno, settore)

WITH settori AS (
    SELECT
        anno,
        'industrie_energetiche' AS settore,
        industrie_energetiche AS emissioni_mt,
        totale
    FROM clean_input
    UNION ALL
    SELECT
        anno,
        'industrie_manifatturiere',
        industrie_manifatturiere,
        totale
    FROM clean_input
    UNION ALL
    SELECT
        anno,
        'residenziale_e_servizi',
        residenziale_e_servizi,
        totale
    FROM clean_input
    UNION ALL
    SELECT
        anno,
        'trasporti',
        trasporti,
        totale
    FROM clean_input
)
SELECT
    anno,
    settore,
    ROUND(emissioni_mt, 2) AS emissioni_mt,
    ROUND(100.0 * emissioni_mt / NULLIF(totale, 0), 2) AS quota_pct
FROM settori
WHERE emissioni_mt IS NOT NULL
ORDER BY anno, settore
