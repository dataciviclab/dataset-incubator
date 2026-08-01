-- mart_trend_settori — Trend emissioni GHG per settore (1990 -> ultimo anno)
--
-- 1 riga = 1 settore (4 settori + totale) con metriche di trend:
-- delta assoluto e % dalla baseline 1990, CAGR annuale, picco e minimo
-- della serie con relativi anni. Serve per: riduzione totale (D1),
-- picco 2005 (D2), -47% industrie energetiche (D3), trasporti in crescita
-- (D4), residenziale stabile (D7), manifatturiero -45% (D8).
--
-- PK: (settore)

WITH settori AS (
    SELECT
        anno,
        'industrie_energetiche' AS settore,
        industrie_energetiche AS emissioni_mt
    FROM clean_input
    UNION ALL
    SELECT anno, 'industrie_manifatturiere', industrie_manifatturiere FROM clean_input
    UNION ALL
    SELECT anno, 'residenziale_e_servizi', residenziale_e_servizi FROM clean_input
    UNION ALL
    SELECT anno, 'trasporti', trasporti FROM clean_input
    UNION ALL
    SELECT anno, 'totale', totale FROM clean_input
),
con_finestre AS (
    SELECT
        anno,
        settore,
        emissioni_mt,
        MIN(anno) OVER (PARTITION BY settore) AS anno_primo,
        MAX(anno) OVER (PARTITION BY settore) AS anno_ultimo
    FROM settori
    WHERE emissioni_mt IS NOT NULL
)
SELECT
    settore,
    MIN(anno_primo) AS anno_primo,
    MAX(anno_ultimo) AS anno_ultimo,
    ROUND(SUM(CASE WHEN anno = anno_primo THEN emissioni_mt END), 1) AS emissioni_1990,
    ROUND(SUM(CASE WHEN anno = anno_ultimo THEN emissioni_mt END), 1) AS emissioni_ultimo,
    ROUND(
        SUM(CASE WHEN anno = anno_ultimo THEN emissioni_mt END)
        - SUM(CASE WHEN anno = anno_primo THEN emissioni_mt END),
        1
    ) AS delta_assoluto_mt,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN emissioni_mt END)
            - SUM(CASE WHEN anno = anno_primo THEN emissioni_mt END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN emissioni_mt END), 0),
        1
    ) AS delta_pct,
    ROUND(
        POWER(
            SUM(CASE WHEN anno = anno_ultimo THEN emissioni_mt END)
            / NULLIF(SUM(CASE WHEN anno = anno_primo THEN emissioni_mt END), 0),
            1.0 / NULLIF(MAX(anno_ultimo) - MIN(anno_primo), 0)
        ) - 1,
        4
    ) AS cagr_annuale,
    ROUND(MAX(emissioni_mt), 1) AS emissioni_picco,
    arg_max(anno, emissioni_mt) AS anno_picco,
    ROUND(MIN(emissioni_mt), 1) AS emissioni_minimo,
    arg_min(anno, emissioni_mt) AS anno_minimo
FROM con_finestre
GROUP BY settore
ORDER BY settore
