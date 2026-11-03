-- clean.sql: immigrazioni per provincia di destinazione (ISTAT
-- 28_185_DF_DCIS_MIGRAZIONI_4 via DBnomics)
--
-- `aggregato` = true per i territori non-standard (livello='aggregato'): le
-- foglie sommabili sono le province.
-- Nomi e classificazione dal support condiviso istat_territori.

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.TERRITORY_NEXT_RESID) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    (t.livello = 'aggregato') as aggregato,
    cast_int(r.OBS_VALUE) as immigrazioni
from raw_input r
left join read_parquet('{support.territori.clean}') t
    on t.ref_area = normalize_string(r.TERRITORY_NEXT_RESID)
where cast_int(r.OBS_VALUE) is not null
