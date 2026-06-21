-- Clean: unified_comuni — multi-anno via S3 glob
-- Ogni fonte prende TUTTI gli anni disponibili (nessuna lista da mantenere).

WITH hub AS (SELECT * FROM raw_input),

pop AS (
    SELECT codice_comune AS cod_istat, anno,
        SUM(popolazione_residente) AS popolazione_residente,
        SUM(totale_maschi) AS maschi,
        SUM(totale_femmine) AS femmine
    FROM read_parquet('s3://dataciviclab-clean/popolazione_istat_comunale_2019_2025/*/popolazione_istat_comunale_2019_2025_*_clean.parquet')
    GROUP BY codice_comune, anno
),

irpef AS (
    SELECT codice_istat_comune AS cod_istat, anno_di_imposta AS anno,
        MAX(numero_contribuenti) AS contribuenti,
        MAX(reddito_imponibile_eur) AS reddito_imponibile_eur,
        MAX(reddito_complessivo_eur) AS reddito_complessivo_eur,
        MAX(imposta_netta_eur) AS imposta_netta_eur,
        MAX(reddito_da_lavoro_dipendente_e_assimilati_eur) AS reddito_lav_dip_eur,
        MAX(reddito_da_pensione_eur) AS reddito_pensione_eur,
        MAX(addizionale_comunale_dovuta_eur) AS addizionale_comunale_eur,
        MAX(addizionale_regionale_dovuta_eur) AS addizionale_regionale_eur
    FROM read_parquet('s3://dataciviclab-clean/irpef_comunale/*/irpef_comunale_*_clean.parquet')
    GROUP BY codice_istat_comune, anno_di_imposta
),

rifiuti AS (
    SELECT RIGHT(codice_comune_istat, 6) AS cod_istat, anno,
        SUM(totale_ru_tonnellate) AS ru_tonnellate,
        SUM(totale_rd_tonnellate) AS rd_tonnellate,
        AVG(percentuale_rd) AS rd_pct
    FROM read_parquet('s3://dataciviclab-clean/ispra_ru_base/*/ispra_ru_base_*_clean.parquet')
    GROUP BY RIGHT(codice_comune_istat, 6), anno
),

consumo_suolo AS (
    SELECT LPAD(CAST(pro_com AS VARCHAR), 6, '0') AS cod_istat,
        stock_ha_2024 AS suolo_consumato_ha,
        stock_pct_2024 AS suolo_consumato_pct,
        incremento_netto_ha_2023_2024 AS suolo_incremento_ha
    FROM read_parquet('s3://dataciviclab-clean/ispra_consumo_suolo/2024/ispra_consumo_suolo_2024_clean.parquet')
),

fsc AS (
    SELECT UPPER(TRIM(comune)) AS denom_upper,
        CAST(popolazione AS INTEGER) AS popolazione_fsc,
        capacita_fiscale,
        dotazione_finale_fsc,
        fondo_perequativo,
        imu_tasi_standard
    FROM read_parquet('s3://dataciviclab-clean/opencivitas_fsc_2025_rso/2025/opencivitas_fsc_2025_rso_2025_clean.parquet')
)

SELECT
    h.codice_istat, p.anno,
    h.denominazione, h.sigla_provincia, h.regione,
    h.superficie_km2, h.altitudine,
    -- Popolazione
    p.popolazione_residente, p.maschi, p.femmine,
    -- IRPEF
    i.contribuenti,
    i.reddito_imponibile_eur, i.reddito_complessivo_eur,
    ROUND(COALESCE(i.reddito_imponibile_eur, i.reddito_complessivo_eur) / NULLIF(p.popolazione_residente, 0), 0) AS reddito_procapite,
    i.reddito_lav_dip_eur, i.reddito_pensione_eur,
    i.imposta_netta_eur,
    i.addizionale_comunale_eur, i.addizionale_regionale_eur,
    -- Rifiuti
    r.ru_tonnellate, r.rd_tonnellate, r.rd_pct,
    ROUND((r.rd_tonnellate * 1000) / NULLIF(p.popolazione_residente, 0), 1) AS rd_procapite_kg,
    -- Consumo suolo
    cs.suolo_consumato_ha, cs.suolo_consumato_pct, cs.suolo_incremento_ha,
    -- FSC
    fsc.popolazione_fsc, fsc.capacita_fiscale, fsc.dotazione_finale_fsc,
    fsc.fondo_perequativo, fsc.imu_tasi_standard
FROM hub h
INNER JOIN pop p ON h.codice_istat = p.cod_istat
LEFT JOIN irpef i ON h.codice_istat = i.cod_istat AND p.anno = i.anno
LEFT JOIN rifiuti r ON h.codice_istat = r.cod_istat AND p.anno = r.anno
LEFT JOIN consumo_suolo cs ON h.codice_istat = cs.cod_istat
LEFT JOIN fsc ON UPPER(TRIM(h.denominazione)) = fsc.denom_upper
ORDER BY h.denominazione, p.anno
