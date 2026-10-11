-- Trend multi-anno per regione (tutti i settori sommati).
-- Usa primo/ultimo anno presenti nel dato, non solo 2024.

WITH reg AS (
    SELECT
        anno,
        regione,
        CASE
            WHEN regione IN (
                'LOMBARDIA', 'PIEMONTE', 'VENETO', 'EMILIA-ROMAGNA', 'TOSCANA',
                'FRIULI VENEZIA GIULIA', 'LIGURIA', 'TRENTINO ALTO ADIGE',
                'VALLE D''AOSTA'
            ) THEN 'nord'
            ELSE 'centro_sud'
        END AS area,
        SUM(accertato) AS accertato
    FROM clean_input
    GROUP BY anno, regione
),
bounds AS (
    SELECT MIN(anno) AS primo, MAX(anno) AS ultimo FROM reg
),
pivoted AS (
    SELECT
        r.regione,
        r.area,
        MAX(CASE WHEN r.anno = b.primo THEN r.accertato END) AS accertato_primo,
        MAX(CASE WHEN r.anno = b.ultimo THEN r.accertato END) AS accertato_ultimo,
        MAX(b.primo) AS anno_primo,
        MAX(b.ultimo) AS anno_ultimo
    FROM reg r
    CROSS JOIN bounds b
    GROUP BY r.regione, r.area
),
ranked AS (
    SELECT
        p.*,
        RANK() OVER (ORDER BY p.accertato_primo DESC) AS rank_primo,
        RANK() OVER (ORDER BY p.accertato_ultimo DESC) AS rank_ultimo
    FROM pivoted p
    WHERE p.accertato_primo IS NOT NULL
      AND p.accertato_ultimo IS NOT NULL
      AND p.accertato_primo <> 0
)
SELECT
    regione,
    area,
    anno_primo,
    anno_ultimo,
    accertato_primo AS accertato_2022,
    accertato_ultimo,
    100.0 * (accertato_ultimo - accertato_primo) / accertato_primo AS delta_pct,
    rank_primo AS rank_2022,
    rank_ultimo,
    rank_ultimo - rank_primo AS delta_rank
FROM ranked
ORDER BY delta_pct DESC
