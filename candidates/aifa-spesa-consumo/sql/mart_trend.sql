-- mart_trend.sql - aifa_spesa_consumo - mart_trend_regione
-- Trend multi-anno: 1 riga = 1 regione sull'intera serie.
--
-- È una tabella multi-anno (`mart.tables[].years` in dataset.yml): il toolkit
-- unisce i clean degli anni dichiarati in `clean_input` e scrive UN solo file
-- a livello dataset, `data/mart/{dataset}/mart_trend_regione.parquet`.
-- Non viene quindi duplicata una copia parziale in ogni cartella anno.
--
-- Conseguenza: il run deve includere tutti gli anni del config (il toolkit
-- solleva FileNotFoundError se manca il clean di un anno dichiarato).

WITH filtro AS (
    -- La fonte usa NULL oppure 0 per le righe senza convenzionata, a seconda
    -- dell'anno: stesso filtro dei mart per-anno.
    SELECT
        anno,
        codreg,
        regione,
        spesa_convenzionata,
        numero_confezioni_convenzionata
    FROM clean_input
    WHERE COALESCE(spesa_convenzionata, 0) <> 0
       OR COALESCE(numero_confezioni_convenzionata, 0) <> 0
),
anni AS (
    SELECT
        anno,
        codreg,
        regione,
        SUM(spesa_convenzionata)             AS spesa,
        SUM(numero_confezioni_convenzionata) AS confezioni
    FROM filtro
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
