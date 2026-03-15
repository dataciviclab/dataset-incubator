-- mart_compose_regioni_v3.sql - compose finale eseguito da sources/a_strutture_asl
-- Input: mart regionali gia aggregati di A, C, D
-- Output: una riga per regione / PA con indicatori di struttura + mortalita evitabile v3
--
-- Nota metodologica v3:
-- - usa le stesse 12 cause Euro-2013 della v2
-- - la mortalita in D e` age-standardized su tre bande 30+:
--   30-69, 70-84, 85+ con pesi ESP2013 aggregati
-- - non usa piu il denominatore ibrido su popolazione totale
-- - la metrica principale esposta qui e` il tasso standardizzato per 100k
-- - fonte B resta fuori dal compose principale

WITH a AS (
    SELECT *
    FROM read_parquet(
        'out/data/mart/malasanita_a_strutture_asl/{year}/mart_regioni.parquet'
    )
),
c AS (
    SELECT *
    FROM read_parquet(
        'out/data/mart/malasanita_c_strutture_ricovero/{year}/mart_regioni.parquet'
    )
),
d AS (
    SELECT *
    FROM read_parquet(
        'out/data/mart/malasanita_d_mortalita_istat/{year}/mart_regioni_v3.parquet'
    )
),
a_lookup AS (
    SELECT
        *,
        CASE codice_regione
            WHEN '041' THEN '21'
            WHEN '042' THEN '22'
            ELSE LEFT(codice_regione, 2)
        END AS cod_territorio_istat
    FROM a
)
SELECT
    a.anno,
    a.codice_regione,
    a.cod_territorio_istat AS cod_territorio,
    a.regione,
    d.territorio AS territorio_istat,

    a.pop_residente,
    a.medici_mmg,
    a.pediatri,
    c.personale_ospedaliero,
    c.medici_ospedalieri,
    c.infermieri,
    c.posti_letto_previsti,
    c.posti_letto_utilizzati,

    d.decessi_evitabili_30plus AS decessi_evitabili_regionali,
    d.pop_media_30plus,
    d.tasso_grezzo_evitabile_10000_30plus,
    d.tasso_std_broad_evitabile_10000_30plus,
    ROUND(d.tasso_std_broad_evitabile_10000_30plus * 10, 2) AS tasso_std_broad_evitabile_100k_30plus,

    a.medici_mmg_per_100k,
    a.pediatri_per_100k,
    ROUND(c.medici_ospedalieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS medici_osp_per_100k,
    ROUND(c.infermieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS infermieri_per_100k,
    ROUND(c.personale_ospedaliero * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS personale_osp_per_100k,
    ROUND(c.posti_letto_previsti * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_previsti_per_100k,
    ROUND(c.posti_letto_utilizzati * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_utilizzati_per_100k,

    CASE WHEN c.codice_regione IS NOT NULL THEN true ELSE false END AS join_c_ok,
    CASE WHEN d.cod_territorio IS NOT NULL THEN true ELSE false END AS join_d_ok
FROM a_lookup a
LEFT JOIN c
    ON a.anno = c.anno
   AND a.codice_regione = c.codice_regione
LEFT JOIN d
    ON a.anno = d.anno
   AND a.cod_territorio_istat = d.cod_territorio
ORDER BY a.codice_regione
