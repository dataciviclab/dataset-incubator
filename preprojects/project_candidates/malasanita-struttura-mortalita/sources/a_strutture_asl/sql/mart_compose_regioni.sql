-- mart_compose_regioni.sql - compose finale eseguito da sources/a_strutture_asl
-- Input: mart regionali gia aggregati di A, C, D
-- Output: una riga per regione / PA con indicatori di struttura + mortalita totale
--
-- Nota metodologica:
-- - questa v1 usa mortalita totale regionale, non mortalita evitabile
-- - il join con D passa da codice_regione a cod_territorio (ultime due cifre)
-- - fonte B resta fuori dal compose della preanalysis

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
        'out/data/mart/malasanita_d_mortalita_istat/{year}/mart_regioni.parquet'
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

    d.decessi_totali AS decessi_totali_regionali,
    d.pop_media_30_plus,
    d.tasso_std_10000_30_plus,
    d.tasso_std_100k_30_plus,

    a.medici_mmg_per_100k,
    a.pediatri_per_100k,
    ROUND(c.medici_ospedalieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS medici_osp_per_100k,
    ROUND(c.infermieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS infermieri_per_100k,
    ROUND(c.personale_ospedaliero * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS personale_osp_per_100k,
    ROUND(c.posti_letto_previsti * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_previsti_per_100k,
    ROUND(c.posti_letto_utilizzati * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS posti_letto_utilizzati_per_100k,
    -- Numeratore 30+ da D, denominatore popolazione totale da A.
    -- Nome esplicito per evitare di farlo leggere come tasso grezzo standard.
    ROUND(d.decessi_totali * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS decessi_30plus_per_100k_pop_totale,

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
