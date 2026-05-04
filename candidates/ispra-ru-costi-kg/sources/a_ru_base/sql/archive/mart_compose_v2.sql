-- mart_compose_v2.sql — ISPRA RU costi kg
--
-- PREREQUISITO: questo SQL richiede un toolkit che espone {root_posix}
-- nel template runtime. I read_parquet seguono l'effective_root del dataset
-- invece di dipendere dal current working directory.
--
-- ORDINE OBBLIGATORIO:
--   1. Materializzare l'anno 2024 prima di qualsiasi altro anno
--   2. Solo dopo eseguire gli altri anni (es. 2020, 2021, 2022, 2023)
--   Motivo: sample_2024 e cluster_lookup_2024 leggono sempre
--   {root_posix}/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet
--   che deve esistere prima che gli altri anni vengano processati.
--
-- SCELTA ANALITICA: le soglie (soglia_rd_2024, soglia_costo_euro_ab_2024)
-- e il cluster demografico sono calcolati sui dati 2024 e usati come
-- riferimento fisso per tutti gli anni. Questo è intenzionale: vogliamo
-- classificare la serie storica rispetto al contesto attuale (2024),
-- non rispetto alle mediane di ogni singolo anno.
-- quadrante_costo è valorizzato solo per anno = 2024.
--
WITH base AS (
    SELECT *
    FROM read_parquet(
        '{root_posix}/data/mart/ispra_ru_base/{year}/mart_cross_comuni.parquet'
    )
),
sample_2024 AS (
    SELECT *
    FROM read_parquet(
        '{root_posix}/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet'
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
        '{root_posix}/data/mart/ispra_ru_base/2024/mart_cross_comuni.parquet'
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
