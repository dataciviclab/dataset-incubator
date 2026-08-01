-- mart_trend_regioni — IVA: trend per regione (primo vs ultimo anno)
--
-- 1 riga = 1 regione: confronto primo vs ultimo anno disponibile della serie.
-- Delta assoluto e % su volume d'affari e contribuenti, plus variazioni di
-- quota. Serve per: crescita regionale nel decennio, divergenza Nord-Sud (D8),
-- anomalie di produttività (D7).
--
-- PK: (regione)

WITH all_clean AS (
    SELECT anno, regione, contribuenti, volume_affari_eur, va_fiscale_eur
    FROM read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name=true
    )
    WHERE anno IS NOT NULL AND regione IS NOT NULL
),
finestre AS (
    SELECT
        regione,
        anno,
        contribuenti,
        volume_affari_eur,
        va_fiscale_eur,
        MIN(anno) OVER (PARTITION BY regione) AS anno_primo,
        MAX(anno) OVER (PARTITION BY regione) AS anno_ultimo
    FROM all_clean
)
SELECT
    regione,
    MAX(anno_primo) AS anno_inizio,
    MAX(anno_ultimo) AS anno_fine,
    SUM(CASE WHEN anno = anno_primo THEN contribuenti END) AS contribuenti_inizio,
    SUM(CASE WHEN anno = anno_ultimo THEN contribuenti END) AS contribuenti_fine,
    ROUND(SUM(CASE WHEN anno = anno_primo THEN volume_affari_eur END), 0) AS volume_inizio_eur,
    ROUND(SUM(CASE WHEN anno = anno_ultimo THEN volume_affari_eur END), 0) AS volume_fine_eur,
    ROUND(
        SUM(CASE WHEN anno = anno_ultimo THEN volume_affari_eur END)
        - SUM(CASE WHEN anno = anno_primo THEN volume_affari_eur END),
        0
    ) AS delta_volume_eur,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN volume_affari_eur END)
            - SUM(CASE WHEN anno = anno_primo THEN volume_affari_eur END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN volume_affari_eur END), 0),
        1
    ) AS delta_volume_pct,
    ROUND(
        100.0 * (
            SUM(CASE WHEN anno = anno_ultimo THEN contribuenti END)
            - SUM(CASE WHEN anno = anno_primo THEN contribuenti END)
        ) / NULLIF(SUM(CASE WHEN anno = anno_primo THEN contribuenti END), 0),
        1
    ) AS delta_contribuenti_pct
FROM finestre
GROUP BY regione
ORDER BY delta_volume_pct DESC
