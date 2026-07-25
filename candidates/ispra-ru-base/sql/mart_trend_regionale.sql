-- ISPRA: Trend RD% per regione 2010-2024
-- RD% medio pesato per regione, con primo anno, ultimo anno, delta assoluto,
-- e CAGR (tasso di crescita annuale composto).
-- Per vedere quali regioni migliorano piu' velocemente.
WITH regioni_anno AS (
    SELECT
        anno,
        regione,
        ROUND(SUM(percentuale_rd * popolazione) / NULLIF(SUM(popolazione), 0), 2) AS rd_media,
        ROUND(SUM(totale_ru_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0), 1) AS kg_ru_procapite,
        ROUND(SUM(totale_rd_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0), 1) AS kg_rd_procapite
    FROM clean_input
    WHERE popolazione > 0 AND regione IS NOT NULL
    GROUP BY anno, regione
),
regioni_trend AS (
    SELECT
        regione,
        MIN(anno) AS primo_anno,
        MAX(anno) AS ultimo_anno,
        MIN(rd_media) FILTER (WHERE anno = (SELECT MIN(anno) FROM regioni_anno r2 WHERE r2.regione = regioni_anno.regione)) AS rd_iniziale,
        MAX(rd_media) FILTER (WHERE anno = (SELECT MAX(anno) FROM regioni_anno r2 WHERE r2.regione = regioni_anno.regione)) AS rd_finale,
        -- pendenza: coefficiente angolare della regressione lineare RD ~ anno
        -- formula: (N*SUM(xy) - SUM(x)*SUM(y)) / (N*SUM(x^2) - SUM(x)^2)
        ROUND(
            (COUNT(*) * SUM(anno * rd_media) - SUM(anno) * SUM(rd_media))
            / NULLIF(COUNT(*) * SUM(anno * anno) - SUM(anno) * SUM(anno), 0)
        , 2) AS pendenza_annuapct
    FROM regioni_anno
    GROUP BY regione
)
SELECT
    t.*,
    ROUND(t.rd_finale - t.rd_iniziale, 2) AS delta_assoluto_punti,
    -- CAGR: (rd_finale/rd_iniziale)^(1/anni) - 1
    CASE
        WHEN t.rd_iniziale > 0 AND t.ultimo_anno > t.primo_anno
        THEN ROUND((POWER(t.rd_finale / t.rd_iniziale, 1.0 / (t.ultimo_anno - t.primo_anno)) - 1) * 100, 2)
        ELSE NULL
    END AS cagr_pct
FROM regioni_trend t
ORDER BY pendenza_annuapct DESC
