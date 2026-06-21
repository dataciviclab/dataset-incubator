-- Clean: unified_comuni
-- Dataset composito: JOIN tra dataset clean via comuni_master.
--
-- Ogni fonte viene caricata dal parquet GCS scaricato nella raw (http_file).
-- Il JOIN usa comuni_master come hub, con le normalizzazioni documentate
-- in registry/join_map.yaml.
--
-- Schema output: una riga per comune × anno, con metriche multi-dominio.
--
-- Fonti attuali:
--   hub:     comuni_master (golden record, ISTAT + IPA)
--   pop:     popolazione_istat_comunale (2019-2025)
--   irpef:   irpef_comunale (2019-2023)
--   ru:      ispra_ru_base (2020-2024)
--   cs:      ispra_consumo_suolo (2024 snapshot)
--   fsc:     opencivitas_fsc_2025_rso (2025)

WITH hub AS (
    SELECT * FROM read_parquet('{root}/data/raw/{dataset}/{year}/hub.parquet')
),

pop AS (
    SELECT
        codice_comune                                      AS cod_istat,
        anno,
        SUM(popolazione_residente)                         AS popolazione_residente,
        SUM(totale_maschi)                                 AS maschi,
        SUM(totale_femmine)                                AS femmine
    FROM read_parquet('{root}/data/raw/{dataset}/{year}/pop.parquet')
    GROUP BY codice_comune, anno
),

irpef AS (
    SELECT
        codice_istat_comune                                AS cod_istat,
        anno_di_imposta                                    AS anno,
        numero_contribuenti,
        reddito_complessivo_eur,
        imposta_netta_eur,
        reddito_da_lavoro_dipendente_e_assimilati_eur      AS reddito_lav_dip_eur,
        reddito_da_pensione_eur,
        addizionale_comunale_dovuta_eur                    AS addizionale_comunale_eur,
        addizionale_regionale_dovuta_eur                   AS addizionale_regionale_eur
    FROM read_parquet('{root}/data/raw/{dataset}/{year}/irpef.parquet')
),

rifiuti AS (
    SELECT
        RIGHT(codice_comune_istat, 6)                      AS cod_istat,
        anno,
        totale_ru_tonnellate,
        totale_rd_tonnellate,
        percentuale_rd
    FROM read_parquet('{root}/data/raw/{dataset}/{year}/ru.parquet')
),

consumo_suolo AS (
    SELECT
        LPAD(CAST(pro_com AS VARCHAR), 6, '0')             AS cod_istat,
        stock_ha_2024                                      AS suolo_consumato_ha,
        stock_pct_2024                                     AS suolo_consumato_pct,
        incremento_netto_ha_2023_2024                      AS suolo_incremento_netto_ha
    FROM read_parquet('{root}/data/raw/{dataset}/{year}/cs.parquet')
),

fsc AS (
    SELECT
        UPPER(TRIM(comune))                                AS denom_upper,
        CAST(popolazione AS INTEGER)                       AS popolazione_fsc,
        capacita_fiscale,
        dotazione_finale_fsc,
        fondo_perequativo,
        imu_tasi_standard,
        totale_risorse_storiche
    FROM read_parquet('{root}/data/raw/{dataset}/{year}/fsc.parquet')
)

SELECT
    -- 🔑 Chiave
    h.codice_istat,
    p.anno                                   AS anno,

    -- 📍 Anagrafica (da hub)
    h.denominazione,
    h.sigla_provincia,
    h.provincia,
    h.regione,
    h.superficie_km2,
    h.altitudine,

    -- 👤 Demografia (da popolazione)
    p.popolazione_residente,
    p.maschi,
    p.femmine,

    -- 💰 Redditi (da IRPEF)
    i.numero_contribuenti,
    i.reddito_complessivo_eur,
    ROUND(i.reddito_complessivo_eur / NULLIF(p.popolazione_residente, 0), 0)
        AS reddito_procapite,
    i.reddito_lav_dip_eur,
    i.reddito_da_pensione_eur,
    i.imposta_netta_eur,
    i.addizionale_comunale_eur,
    i.addizionale_regionale_eur,

    -- 🗑️ Rifiuti (da ISPRA)
    r.totale_ru_tonnellate,
    r.totale_rd_tonnellate,
    r.percentuale_rd,
    ROUND((r.totale_rd_tonnellate * 1000) / NULLIF(p.popolazione_residente, 0), 1)
        AS rd_procapite_kg,

    -- 🌍 Consumo suolo (da ISPRA)
    cs.suolo_consumato_ha,
    cs.suolo_consumato_pct,
    cs.suolo_incremento_netto_ha,

    -- 💸 FSC (da OpenCivitas)
    fsc.popolazione_fsc,
    fsc.capacita_fiscale,
    fsc.dotazione_finale_fsc,
    fsc.fondo_perequativo,
    fsc.imu_tasi_standard

FROM hub h
-- Popolazione: tutti i comuni, solo anni con dati
LEFT JOIN pop p
    ON h.codice_istat = p.cod_istat
-- IRPEF: stesso anno della popolazione
LEFT JOIN irpef i
    ON h.codice_istat = i.cod_istat AND p.anno = i.anno
-- Rifiuti: stesso anno
LEFT JOIN rifiuti r
    ON h.codice_istat = r.cod_istat AND p.anno = r.anno
-- Consumo suolo: dataset singolo anno, join su codice
LEFT JOIN consumo_suolo cs
    ON h.codice_istat = cs.cod_istat
-- FSC: join su denominazione
LEFT JOIN fsc
    ON UPPER(TRIM(h.denominazione)) = fsc.denom_upper
-- Solo comuni con dati popolazione (filtra righe vuote)
WHERE p.anno IS NOT NULL
ORDER BY h.denominazione, p.anno
