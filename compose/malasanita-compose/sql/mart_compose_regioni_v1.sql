-- mart_compose_regioni_v1.sql - compose puro malasanita
-- Input: mart regionali di A (strutture-asl), C (strutture-ricovero-asl), D (mortalita-istat-evitabile)
-- Output: una riga per regione / PA con indicatori di struttura + mortalita totale 30+
--
-- Baseline v1: mortalita totale 30+ (cod_causa=25) da D v1
-- Fonte B (reparti-ricovero) resta fuori dal compose principale.

WITH a AS (
    SELECT *
    FROM read_parquet('{support.a.mart}')
),
c AS (
    SELECT *
    FROM read_parquet('{support.c.mart}')
),
d AS (
    SELECT *
    FROM read_parquet('out/data/mart/mortalita_istat_evitabile/{year}/mart_regioni_v1.parquet')
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

    d.decessi_30plus AS decessi_regionali,
    d.pop_media_30plus,
    d.tasso_grezzo_10000_30plus,

    a.medici_mmg_per_100k,
    a.pediatri_per_100k,
    ROUND(c.medici_ospedalieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS medici_osp_per_100k,
    ROUND(c.infermieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS infermieri_per_100k,
    ROUND(c.personale_ospedaliero * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS personale_osp_per_100k,
    ROUND(c.posti_letto_previsti * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_previsti_per_100k,
    ROUND(c.posti_letto_utilizzati * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_utilizzati_per_100k,
    ROUND(d.decessi_30plus * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS decessi_30plus_per_100k_pop_totale,

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
