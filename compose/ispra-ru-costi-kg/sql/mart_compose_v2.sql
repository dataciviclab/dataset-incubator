-- mart_compose_v2.sql — ISPRA RU costi kg (compose)
--
-- Layer analitico: soglie, cluster, quadranti.
-- Dipende da mart_cross_comuni generato dallo stesso compose.
-- Usa {year} dinamico invece di path hardcodati.
WITH base AS (
    SELECT *
    FROM read_parquet(
        '{root_posix}/data/mart/ispra_ru_costi_kg_compose/{year}/mart_cross_comuni.parquet'
    )
),
sample_year AS (
    SELECT *
    FROM base
    WHERE join_b_ok
      AND join_c_ok
      AND percentuale_rd IS NOT NULL
      AND costo_totale_euro_ab IS NOT NULL
),
thresholds AS (
    SELECT
        median(percentuale_rd) AS soglia_rd,
        median(costo_totale_euro_ab) AS soglia_costo_euro_ab
    FROM sample_year
),
cluster_lookup AS (
    SELECT DISTINCT
        codice_comune_istat,
        CASE
            WHEN popolazione IS NULL THEN 'N/D'
            WHEN popolazione < 5000 THEN '<5k'
            WHEN popolazione < 20000 THEN '5k-20k'
            WHEN popolazione < 100000 THEN '20k-100k'
            ELSE '>100k'
        END AS cluster_demografico
    FROM base
)
SELECT
    base.*,
    CASE
        WHEN base.regione IN (
            'Piemonte', 'Valle d''Aosta', 'Liguria', 'Lombardia',
            'Trentino-Alto Adige', 'Veneto', 'Friuli-Venezia Giulia', 'Emilia-Romagna'
        ) THEN 'Nord'
        WHEN base.regione IN (
            'Toscana', 'Umbria', 'Marche', 'Lazio'
        ) THEN 'Centro'
        WHEN base.regione IN (
            'Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata',
            'Calabria', 'Sicilia', 'Sardegna'
        ) THEN 'Sud'
        ELSE 'N/D'
    END AS regione_macro,
    cluster_lookup.cluster_demografico,
    thresholds.soglia_rd AS soglia_rd_anno,
    thresholds.soglia_costo_euro_ab AS soglia_costo_euro_ab_anno,
    CASE
        WHEN base.join_b_ok AND base.join_c_ok
         AND base.percentuale_rd IS NOT NULL
         AND base.costo_totale_euro_ab IS NOT NULL
            THEN base.percentuale_rd >= thresholds.soglia_rd
        ELSE NULL
    END AS rd_alta,
    CASE
        WHEN base.join_b_ok AND base.join_c_ok
         AND base.percentuale_rd IS NOT NULL
         AND base.costo_totale_euro_ab IS NOT NULL
            THEN base.costo_totale_euro_ab >= thresholds.soglia_costo_euro_ab
        ELSE NULL
    END AS costo_alto,
    CASE
        WHEN NOT base.join_b_ok OR NOT base.join_c_ok THEN 'Dati mancanti'
        WHEN base.percentuale_rd IS NULL OR base.costo_totale_euro_ab IS NULL THEN 'Dati mancanti'
        WHEN base.percentuale_rd >= thresholds.soglia_rd
         AND base.costo_totale_euro_ab < thresholds.soglia_costo_euro_ab
            THEN 'Virtuoso costo-performance (RD alta, costo basso)'
        WHEN base.percentuale_rd >= thresholds.soglia_rd
         AND base.costo_totale_euro_ab >= thresholds.soglia_costo_euro_ab
            THEN 'Buona performance ma costo alto (RD alta, costo alto)'
        WHEN base.percentuale_rd < thresholds.soglia_rd
         AND base.costo_totale_euro_ab < thresholds.soglia_costo_euro_ab
            THEN 'Costo contenuto ma performance debole (RD bassa, costo basso)'
        ELSE 'Criticità su entrambi gli assi (RD bassa, costo alto)'
    END AS quadrante_costo
FROM base
LEFT JOIN cluster_lookup
    ON base.codice_comune_istat = cluster_lookup.codice_comune_istat
CROSS JOIN thresholds
ORDER BY base.regione, base.provincia, base.comune
