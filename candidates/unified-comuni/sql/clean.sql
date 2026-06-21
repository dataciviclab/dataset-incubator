-- Clean: unified_comuni — multi-anno via S3 glob
-- Hub da raw_input, fonti dati lette da GCS via S3 glob.
-- Ogni fonte prende TUTTI gli anni disponibili (nessuna lista da mantenere).

WITH hub AS (SELECT * FROM raw_input),

pop AS (
    SELECT codice_comune AS cod_istat, anno,
        SUM(popolazione_residente) AS popolazione_residente
    FROM read_parquet('s3://dataciviclab-clean/popolazione_istat_comunale_2019_2025/*/popolazione_istat_comunale_2019_2025_*_clean.parquet')
    GROUP BY codice_comune, anno
),

irpef AS (
    SELECT codice_istat_comune AS cod_istat, anno_di_imposta AS anno,
        MAX(numero_contribuenti) AS contribuenti,
        MAX(reddito_imponibile_eur) AS reddito_imponibile_eur
    FROM read_parquet('s3://dataciviclab-clean/irpef_comunale/*/irpef_comunale_*_clean.parquet')
    GROUP BY codice_istat_comune, anno_di_imposta
),

rifiuti AS (
    SELECT RIGHT(codice_comune_istat, 6) AS cod_istat, anno,
        SUM(totale_ru_tonnellate) AS ru_tot,
        AVG(percentuale_rd) AS rd_pct
    FROM read_parquet('s3://dataciviclab-clean/ispra_ru_base/*/ispra_ru_base_*_clean.parquet')
    GROUP BY RIGHT(codice_comune_istat, 6), anno
),

fsc AS (
    SELECT UPPER(TRIM(comune)) AS denom,
        dotazione_finale_fsc
    FROM read_parquet('s3://dataciviclab-clean/opencivitas_fsc_2025_rso/2025/opencivitas_fsc_2025_rso_2025_clean.parquet')
)

SELECT h.codice_istat, p.anno,
    h.denominazione, h.sigla_provincia, h.regione,
    p.popolazione_residente,
    i.contribuenti, i.reddito_imponibile_eur,
    r.ru_tot, r.rd_pct,
    fsc.dotazione_finale_fsc
FROM hub h
INNER JOIN pop p ON h.codice_istat = p.cod_istat
LEFT JOIN irpef i ON h.codice_istat = i.cod_istat AND p.anno = i.anno
LEFT JOIN rifiuti r ON h.codice_istat = r.cod_istat AND p.anno = r.anno
LEFT JOIN fsc ON UPPER(TRIM(h.denominazione)) = fsc.denom
ORDER BY h.denominazione, p.anno
