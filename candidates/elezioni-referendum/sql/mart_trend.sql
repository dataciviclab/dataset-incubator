-- Mart: trend affluenza referendaria per regione (2011-2022)
-- Legge da tutti i clean parquet locali via glob (pattern standard Lab).
-- Solo dal 2011: tornate pre-2011 hanno solo dato provinciale (comune=NULL).

WITH tutti_anni AS (
    SELECT * FROM read_parquet(
        '{root}/data/clean/elezioni_referendum/*/elezioni_referendum_*_clean.parquet',
        union_by_name=true
    )
    WHERE comune IS NOT NULL AND comune != ''
),

affluenza_regione AS (
    SELECT
        EXTRACT(YEAR FROM data_elezione) AS anno,
        regione,
        ROUND(AVG(CAST(votanti AS DOUBLE) / NULLIF(CAST(elettori AS DOUBLE), 0) * 100), 2) AS affluenza_media_pct,
        COUNT(DISTINCT comune) AS comuni
    FROM tutti_anni
    GROUP BY EXTRACT(YEAR FROM data_elezione), regione
),

finestre AS (
    SELECT regione,
        MIN(anno) AS primo_anno,
        MAX(anno) AS ultimo_anno
    FROM affluenza_regione
    GROUP BY regione
)

SELECT
    ar.regione,
    ar.anno,
    ar.affluenza_media_pct,
    ar.comuni,
    f.primo_anno,
    f.ultimo_anno
FROM affluenza_regione ar
LEFT JOIN finestre f ON ar.regione = f.regione
ORDER BY ar.regione, ar.anno
