-- Clean: unified_comuni — multi-anno via HTTPS diretto
-- DuckDB 1.5.4 legge https://storage.googleapis.com/ nativamente,
-- senza estensioni httpfs. Niente bug S3, niente config.
-- union_by_name=true gestisce eterogeneità colonne tra anni.
--
-- Policy manutenzione: quando si aggiunge un anno, aggiungere l'URL
-- o estendere il glob. Per dataset multi-anno si elencano tutti.
--
-- Domini integrati:
--   hub (comuni_master) + popolazione + IRPEF + rifiuti
--   + consumo suolo (solo 2024, cross-anno)
--   + Fondo Solidarietà Comunale (join testuale denominazione+regione)
--   + SIOPE (via bridge bdap_anagrafe_enti.codice_ente_siope)
--   + Dipendenti PA (via bridge bdap_anagrafe_enti.id_ente, dati fino 2023)
--   + PNRR (via comuni_master.codice_fiscale)
--
-- Note sui join testuali (denominazione):
--   - FSC non ha codice_istat, join su denominazione+regione.
--     Fragile per fusioni/omonimie. Cross-validato con regione.

WITH hub AS (
    SELECT * FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/comuni_master/2026/comuni_master_2026_clean.parquet', union_by_name=true)
),

-- Bridge table: mappa codici SIOPE e BDAP a codice_istat
bridge AS (
    SELECT codice_ente_siope, codice_istat_comune, id_ente
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/bdap_anagrafe_enti/2026/bdap_anagrafe_enti_2026_clean.parquet', union_by_name=true)
    WHERE codice_istat_comune IS NOT NULL
),

pop AS (
    SELECT codice_comune AS cod_istat, anno,
        SUM(popolazione_residente) AS popolazione_residente,
        SUM(totale_maschi) AS maschi,
        SUM(totale_femmine) AS femmine
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2019/popolazione_istat_comunale_2019_2025_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2020/popolazione_istat_comunale_2019_2025_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2021/popolazione_istat_comunale_2019_2025_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2022/popolazione_istat_comunale_2019_2025_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2023/popolazione_istat_comunale_2019_2025_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2024/popolazione_istat_comunale_2019_2025_2024_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/popolazione_istat_comunale_2019_2025/2025/popolazione_istat_comunale_2019_2025_2025_clean.parquet'
    ], union_by_name=true)
    GROUP BY codice_comune, anno
),

irpef AS (
    SELECT codice_istat_comune AS cod_istat, anno_di_imposta AS anno,
        -- ANY_VALUE è sicuro: IRPEF ha 1 riga per comune/anno
        ANY_VALUE(numero_contribuenti) AS contribuenti,
        ANY_VALUE(reddito_imponibile_eur) AS reddito_imponibile_eur,
        ANY_VALUE(reddito_complessivo_eur) AS reddito_complessivo_eur,
        ANY_VALUE(imposta_netta_eur) AS imposta_netta_eur,
        ANY_VALUE(reddito_da_lavoro_dipendente_e_assimilati_eur) AS reddito_lav_dip_eur,
        ANY_VALUE(reddito_da_pensione_eur) AS reddito_pensione_eur,
        ANY_VALUE(addizionale_comunale_dovuta_eur) AS addizionale_comunale_eur,
        ANY_VALUE(addizionale_regionale_dovuta_eur) AS addizionale_regionale_eur
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2019/irpef_comunale_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2020/irpef_comunale_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2021/irpef_comunale_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2022/irpef_comunale_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2023/irpef_comunale_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/irpef_comunale/2024/irpef_comunale_2024_clean.parquet'
    ], union_by_name=true)
    GROUP BY codice_istat_comune, anno_di_imposta
),

rifiuti AS (
    SELECT RIGHT(codice_comune_istat, 6) AS cod_istat, anno,
        SUM(totale_ru_tonnellate) AS ru_tonnellate,
        SUM(totale_rd_tonnellate) AS rd_tonnellate,
        AVG(percentuale_rd) AS rd_pct
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/ispra_ru_base/2020/ispra_ru_base_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/ispra_ru_base/2021/ispra_ru_base_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/ispra_ru_base/2022/ispra_ru_base_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/ispra_ru_base/2023/ispra_ru_base_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/ispra_ru_base/2024/ispra_ru_base_2024_clean.parquet'
    ], union_by_name=true)
    GROUP BY RIGHT(codice_comune_istat, 6), anno
),

consumo_suolo AS (
    SELECT LPAD(CAST(pro_com AS VARCHAR), 6, '0') AS cod_istat,
        anno,
        stock_ha AS suolo_consumato_ha,
        stock_pct AS suolo_consumato_pct,
        incremento_netto_ha AS suolo_incremento_ha
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/ispra_consumo_suolo/2024/ispra_consumo_suolo_2024_clean.parquet', union_by_name=true)
),

fsc AS (
    SELECT UPPER(TRIM(comune)) AS denom_upper,
        regione,
        anno,
        CAST(popolazione AS INTEGER) AS popolazione_fsc,
        capacita_fiscale,
        dotazione_finale_fsc,
        fondo_perequativo,
        imu_tasi_standard
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/opencivitas_fsc_2025_rso/2022/opencivitas_fsc_2025_rso_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/opencivitas_fsc_2025_rso/2023/opencivitas_fsc_2025_rso_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/opencivitas_fsc_2025_rso/2024/opencivitas_fsc_2025_rso_2024_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/opencivitas_fsc_2025_rso/2025/opencivitas_fsc_2025_rso_2025_clean.parquet'
    ], union_by_name=true)
),

-- SIOPE: join via bdap_anagrafe_enti.codice_ente_siope
-- Filtra solo comuni (tipo_ente='COMUNE' implicitamente via bridge)
siope AS (
    SELECT b.codice_istat_comune AS cod_istat, s.anno,
        SUM(CASE WHEN s.lato='entrate' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_entrate,
        SUM(CASE WHEN s.lato='uscite' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_uscite,
        SUM(CASE WHEN s.lato='uscite' AND s.macro_categoria='Personale' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_personale,
        SUM(CASE WHEN s.lato='uscite' AND s.macro_categoria='Investimenti' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_investimenti,
        SUM(CASE WHEN s.lato='entrate' AND s.macro_categoria_v2='Imposte proprie' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_imposte_proprie,
        SUM(CASE WHEN s.lato='entrate' AND s.macro_categoria_v2='Fondi perequativi' AND NOT s.is_titolo_9 THEN s.importo_eur ELSE 0 END) AS siope_fondi_perequativi
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/siope_bilancio_unificato/2021/siope_bilancio_unificato_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/siope_bilancio_unificato/2022/siope_bilancio_unificato_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/siope_bilancio_unificato/2023/siope_bilancio_unificato_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/siope_bilancio_unificato/2024/siope_bilancio_unificato_2024_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/siope_bilancio_unificato/2025/siope_bilancio_unificato_2025_clean.parquet'
    ], union_by_name=true) s
    INNER JOIN bridge b ON s.codice_ente = b.codice_ente_siope
    GROUP BY b.codice_istat_comune, s.anno
),

-- Dipendenti PA: join via bdap_anagrafe_enti.id_ente
-- Dati disponibili solo fino al 2023. Per anni > 2023 sarà NULL.
dipendenti AS (
    SELECT b.codice_istat_comune AS cod_istat, d.anno,
        SUM(d.donne_tempo_pieno + d.uomini_tempo_pieno
            + d.donne_part_time_inf_50 + d.uomini_part_time_inf_50
            + d.donne_part_time_sup_50 + d.uomini_part_time_sup_50) AS dipendenti_totali,
        SUM(d.donne_assunte + d.uomini_assunti) AS dipendenti_assunti,
        SUM(d.donne_cessate + d.uomini_cessati) AS dipendenti_cessati
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/dipendenti_pubblici/2019/dipendenti_pubblici_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/dipendenti_pubblici/2020/dipendenti_pubblici_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/dipendenti_pubblici/2021/dipendenti_pubblici_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/dipendenti_pubblici/2022/dipendenti_pubblici_2022_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/dipendenti_pubblici/2023/dipendenti_pubblici_2023_clean.parquet'
    ], union_by_name=true) d
    INNER JOIN bridge b ON CAST(d.codice_ente_bdap AS VARCHAR) = CAST(b.id_ente AS VARCHAR)
    GROUP BY b.codice_istat_comune, d.anno
),

-- PNRR: join via comuni_master.codice_fiscale
pnrr AS (
    SELECT h.codice_istat AS cod_istat,
        COUNT(*) AS pnrr_progetti,
        SUM(p.fin_totale) AS pnrr_fin_totale
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/pnrr_progetti/2026/pnrr_progetti_2026_clean.parquet', union_by_name=true) p
    INNER JOIN hub h ON p.cf_soggetto_attuatore = h.codice_fiscale
    GROUP BY h.codice_istat
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
    -- Consumo suolo (dato 2024, cross-anno)
    cs.suolo_consumato_ha, cs.suolo_consumato_pct, cs.suolo_incremento_ha,
    -- FSC (join testuale denominazione+regione)
    fsc.popolazione_fsc, fsc.capacita_fiscale, fsc.dotazione_finale_fsc,
    fsc.fondo_perequativo, fsc.imu_tasi_standard,
    -- SIOPE (via bridge bdap)
    s.siope_entrate, s.siope_uscite,
    s.siope_entrate - s.siope_uscite AS siope_avanzo,
    s.siope_personale, s.siope_investimenti,
    s.siope_imposte_proprie, s.siope_fondi_perequativi,
    -- Dipendenti PA (fino 2023 via bridge bdap)
    d.dipendenti_totali, d.dipendenti_assunti, d.dipendenti_cessati,
    d.dipendenti_assunti - d.dipendenti_cessati AS dipendenti_saldo,
    -- PNRR (via codice_fiscale)
    pn.pnrr_progetti, pn.pnrr_fin_totale
FROM hub h
INNER JOIN pop p ON h.codice_istat = p.cod_istat
LEFT JOIN irpef i ON h.codice_istat = i.cod_istat AND p.anno = i.anno
LEFT JOIN rifiuti r ON h.codice_istat = r.cod_istat AND p.anno = r.anno
LEFT JOIN consumo_suolo cs ON h.codice_istat = cs.cod_istat AND p.anno = cs.anno
LEFT JOIN fsc ON UPPER(TRIM(h.denominazione)) = fsc.denom_upper
    AND UPPER(TRIM(h.regione)) = UPPER(TRIM(fsc.regione))
    AND p.anno = fsc.anno
LEFT JOIN siope s ON h.codice_istat = s.cod_istat AND p.anno = s.anno
LEFT JOIN dipendenti d ON h.codice_istat = d.cod_istat AND p.anno = d.anno
LEFT JOIN pnrr pn ON h.codice_istat = pn.cod_istat
ORDER BY h.denominazione, p.anno
