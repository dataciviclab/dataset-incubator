-- NOTE OPERATIVA:
-- Questo mart usa intenzionalmente il 2024 come lookup fisso per:
-- 1. calcolare le mediane del quadrante_costo;
-- 2. derivare il cluster_demografico dal mart_cross_comuni 2024.
--
-- Conseguenza: su un clone fresco va materializzato prima il 2024 e solo dopo
-- gli altri anni. I path read_parquet sotto out/... riflettono il vincolo
-- operativo attuale del toolkit e restano un punto da migliorare in un follow-up.

WITH base AS (
    SELECT *
    FROM read_parquet(
        'out/data/mart/ispra_ru_base/{year}/mart_cross_comuni.parquet'
    )
),
sample_2024 AS (
    SELECT *
    FROM read_parquet(
        'out/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet'
    )
    WHERE join_b_ok
      AND join_c_ok
      AND percentuale_rd IS NOT NULL
      AND costo_totale_euro_ab IS NOT NULL
),
thresholds AS (
    SELECT
        median(percentuale_rd) AS soglia_rd_2024,
        median(costo_totale_euro_ab) AS soglia_costo_euro_ab_2024
    FROM sample_2024
),
cluster_lookup_2024 AS (
    SELECT DISTINCT
        codice_comune_istat,
        CASE
            WHEN popolazione IS NULL THEN 'N/D'
            WHEN popolazione < 5000 THEN '<5k'
            WHEN popolazione < 20000 THEN '5k-20k'
            WHEN popolazione < 100000 THEN '20k-100k'
            ELSE '>100k'
        END AS cluster_demografico
    FROM read_parquet(
        'out/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet'
    )
)
SELECT
    base.*,
    CASE
        WHEN base.regione IN (
            'Piemonte',
            'Valle d''Aosta',
            'Liguria',
            'Lombardia',
            'Trentino-Alto Adige',
            'Veneto',
            'Friuli-Venezia Giulia',
            'Emilia-Romagna'
        ) THEN 'Nord'
        WHEN base.regione IN (
            'Toscana',
            'Umbria',
            'Marche',
            'Lazio'
        ) THEN 'Centro'
        WHEN base.regione IN (
            'Abruzzo',
            'Molise',
            'Campania',
            'Puglia',
            'Basilicata',
            'Calabria',
            'Sicilia',
            'Sardegna'
        ) THEN 'Sud'
        ELSE 'N/D'
    END AS regione_macro,
    cluster_lookup_2024.cluster_demografico,
    thresholds.soglia_rd_2024,
    thresholds.soglia_costo_euro_ab_2024,
    CASE
        WHEN base.anno = 2024
         AND base.join_b_ok
         AND base.join_c_ok
         AND base.percentuale_rd IS NOT NULL
         AND base.costo_totale_euro_ab IS NOT NULL
            THEN base.percentuale_rd >= thresholds.soglia_rd_2024
        ELSE NULL
    END AS rd_alta_2024,
    CASE
        WHEN base.anno = 2024
         AND base.join_b_ok
         AND base.join_c_ok
         AND base.percentuale_rd IS NOT NULL
         AND base.costo_totale_euro_ab IS NOT NULL
            THEN base.costo_totale_euro_ab >= thresholds.soglia_costo_euro_ab_2024
        ELSE NULL
    END AS costo_alto_2024,
    CASE
        WHEN base.anno <> 2024 THEN NULL
        WHEN NOT base.join_b_ok OR NOT base.join_c_ok THEN 'Dati mancanti'
        WHEN base.percentuale_rd IS NULL OR base.costo_totale_euro_ab IS NULL THEN 'Dati mancanti'
        WHEN base.percentuale_rd >= thresholds.soglia_rd_2024
         AND base.costo_totale_euro_ab < thresholds.soglia_costo_euro_ab_2024
            THEN 'Virtuoso costo-performance (RD alta, costo basso)'
        WHEN base.percentuale_rd >= thresholds.soglia_rd_2024
         AND base.costo_totale_euro_ab >= thresholds.soglia_costo_euro_ab_2024
            THEN 'Buona performance ma costo alto (RD alta, costo alto)'
        WHEN base.percentuale_rd < thresholds.soglia_rd_2024
         AND base.costo_totale_euro_ab < thresholds.soglia_costo_euro_ab_2024
            THEN 'Costo contenuto ma performance debole (RD bassa, costo basso)'
        ELSE 'Criticità su entrambi gli assi (RD bassa, costo alto)'
    END AS quadrante_costo
FROM base
LEFT JOIN cluster_lookup_2024
    ON base.codice_comune_istat = cluster_lookup_2024.codice_comune_istat
CROSS JOIN thresholds
ORDER BY base.regione, base.provincia, base.comune
