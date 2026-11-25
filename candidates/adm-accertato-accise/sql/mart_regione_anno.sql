-- Grato: regione x anno x settore, con quota nazionale e rank per settore.
-- area: macro-nord / centro-sud per confronto aggregato (non unità geostatistica).

WITH base AS (
    SELECT
        anno,
        settore,
        regione,
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
),
with_share AS (
    SELECT
        b.*,
        100.0 * b.accertato_totale / SUM(b.accertato_totale) OVER (PARTITION BY b.anno) AS quota_pct_naz,
        RANK() OVER (PARTITION BY b.anno, b.settore ORDER BY b.accertato_totale DESC) AS rank_settore
    FROM base b
)
SELECT
    anno,
    settore,
    regione,
    area,
    accertato_totale,
    quota_pct_naz,
    rank_settore
FROM with_share
