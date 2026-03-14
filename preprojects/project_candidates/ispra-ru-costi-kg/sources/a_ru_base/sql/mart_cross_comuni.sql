WITH a AS (
    SELECT
        {year} AS anno,
        *
    FROM read_parquet(
        'out/data/mart/ispra_ru_base/{year}/mart_comuni.parquet'
    )
),
b AS (
    SELECT
        {year} AS anno,
        *
    FROM read_parquet(
        'out/data/mart/ispra_ru_costi_kg/{year}/mart_comuni.parquet'
    )
),
c AS (
    SELECT
        {year} AS anno,
        *
    FROM read_parquet(
        'out/data/mart/ispra_ru_costi_procapite/{year}/mart_comuni.parquet'
    )
)
SELECT
    a.anno,
    a.codice_comune_istat,
    a.regione,
    a.provincia,
    a.comune,
    a.popolazione,

    a.totale_ru_tonnellate,
    a.totale_rd_tonnellate,
    a.percentuale_rd,
    a.kg_ru_per_abitante_calc,
    a.kg_rd_per_abitante_calc,

    b.ctot_cent_kg AS costo_totale_cent_kg,
    b.crt_cent_kg,
    b.crd_cent_kg,
    b.csl_cent_kg,
    b.cc_cent_kg,
    b.ck_cent_kg,

    c.ctot_euro_ab AS costo_totale_euro_ab,
    c.crt_euro_ab,
    c.cts_euro_ab,
    c.crd_euro_ab,
    c.ctr_euro_ab,
    c.csl_euro_ab,
    c.cc_euro_ab,
    c.ck_euro_ab,
    c.altri_costi_euro_ab,

    ROUND(a.totale_ru_tonnellate * 1000.0 / NULLIF(a.popolazione, 0), 3) AS kg_ru_per_abitante_recomputed,

    CASE WHEN b.codice_comune_istat IS NOT NULL THEN true ELSE false END AS join_b_ok,
    CASE WHEN c.codice_comune_istat IS NOT NULL THEN true ELSE false END AS join_c_ok
FROM a
LEFT JOIN b
    ON a.anno = b.anno
   AND a.codice_comune_istat = b.codice_comune_istat
LEFT JOIN c
    ON a.anno = c.anno
   AND a.codice_comune_istat = c.codice_comune_istat
ORDER BY a.regione, a.provincia, a.comune
