-- clean: UNION ALL di entrate e uscite SIOPE
-- raw_input = entrate (primary source)
-- uscite letta direttamente da GCS
-- Le colonne divergenti vengono allineate con NULL

with entrate as (
    select
        codice_comparto, anno, periodo,
        codice_ente, codice_voce,
        denominazione_ente, tipo_ente,
        codice_istat_comune,
        codice_provincia, provincia, regione,
        codice_sottocomparto, descrizione_sottocomparto,
        descrizione_comparto,
        is_titolo_9, macro_categoria_v2,
        null::varchar as macro_area,
        null::varchar as macro_categoria,
        descrizione_codice,
        has_codgest_match,
        importo, importo_eur,
        'entrate'::varchar as lato
    from raw_input
),
uscite as (
    select
        codice_comparto, anno, periodo,
        codice_ente, codice_voce,
        denominazione_ente, tipo_ente,
        codice_istat_comune,
        codice_provincia, provincia, regione,
        codice_sottocomparto, descrizione_sottocomparto,
        descrizione_comparto,
        is_titolo_9,
        null::varchar as macro_categoria_v2,
        macro_area,
        macro_categoria,
        descrizione_codice,
        has_codgest_match,
        importo, importo_eur,
        'uscite'::varchar as lato
    from read_parquet('https://storage.googleapis.com/dataciviclab-clean/siope/siope_uscite/{year}/siope_uscite_{year}_clean.parquet')
)
select * from entrate
union all
select * from uscite;
