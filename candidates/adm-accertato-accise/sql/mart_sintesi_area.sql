-- Sintesi nord/centro-sud x anno x settore + quote sul totale nazionale.

WITH base AS (
    SELECT
        anno,
        settore,
        CASE
            WHEN regione IN (
                'LOMBARDIA', 'PIEMONTE', 'VENETO', 'EMILIA-ROMAGNA', 'TOSCANA',
                'FRIULI VENEZIA GIULIA', 'LIGURIA', 'TRENTINO ALTO ADIGE',
                'VALLE D''AOSTA'
            ) THEN 'nord'
            ELSE 'centro_sud'
        END AS area,
        SUM(accertato) AS accertato_totale
    FROM clean_input
    GROUP BY anno, settore, regione
)
SELECT
    anno,
    area,
    settore,
    SUM(accertato_totale) AS accertato_totale,
    100.0 * SUM(accertato_totale) / SUM(SUM(accertato_totale)) OVER (PARTITION BY anno) AS quota_pct
FROM base
GROUP BY anno, area, settore
