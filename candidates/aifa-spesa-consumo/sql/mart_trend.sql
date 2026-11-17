-- mart_trend.sql - aifa_spesa_consumo - mart_trend_regione
-- Trend multi-anno: 1 riga = 1 regione sull'intera serie disponibile.
-- Legge TUTTI gli anni dal clean via glob (pattern toolkit {root}/{dataset}),
-- quindi il risultato non dipende dall'anno del run.

WITH all_clean AS (
    SELECT
        anno,
        codreg,
        regione,
        spesa_convenzionata,
        numero_confezioni_convenzionata
    FROM read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name = true
    )
    WHERE spesa_convenzionata IS NOT NULL
),
anni AS (
    SELECT
        anno,
        codreg,
        regione,
        SUM(spesa_convenzionata)             AS spesa,
        SUM(numero_confezioni_convenzionata) AS confezioni
    FROM all_clean
    GROUP BY anno, codreg, regione
),
serie AS (
    SELECT
        codreg,
        regione,
        MIN(anno)                     AS anno_primo,
        MAX(anno)                     AS anno_ultimo,
        COUNT(*)                      AS n_anni,
        MIN_BY(spesa, anno)           AS spesa_primo,
        MAX_BY(spesa, anno)           AS spesa_ultimo,
        MIN_BY(confezioni, anno)      AS confezioni_prime,
        MAX_BY(confezioni, anno)      AS confezioni_ultime
    FROM anni
    GROUP BY codreg, regione
)
SELECT
    codreg,
    regione,
    anno_primo,
    anno_ultimo,
    n_anni,
    ROUND(spesa_primo, 2)                                             AS spesa_primo_anno,
    ROUND(spesa_ultimo, 2)                                            AS spesa_ultimo_anno,
    ROUND((spesa_ultimo / NULLIF(spesa_primo, 0) - 1) * 100, 2)       AS delta_spesa_pct,
    ROUND(
        (POWER(spesa_ultimo / NULLIF(spesa_primo, 0), 1.0 / NULLIF(n_anni - 1, 0)) - 1) * 100,
        2
    )                                                                 AS cagr_spesa_pct,
    ROUND(spesa_ultimo / NULLIF(confezioni_ultime, 0), 2)             AS costo_medio_ultimo_anno
FROM serie
ORDER BY regione
