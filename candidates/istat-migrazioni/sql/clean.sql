-- clean.sql: immigrazioni per provincia di destinazione (ISTAT
-- 28_185_DF_DCIS_MIGRAZIONI_4 via DBnomics)
--
-- Grano: anno x territorio di destinazione (nazionale/ripartizione/regione/
-- provincia). Nomi da codelist locale (estratto dal metadata DBnomics).
-- Slice: cittadinanza/età/sesso/motivo = totale (solo il totale dei flussi).

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.TERRITORY_NEXT_RESID) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    cast_int(r.OBS_VALUE) as immigrazioni
from raw_input r
left join read_csv(
    'candidates/istat-migrazioni/codelists/istat_territori.csv',
    auto_detect=true, header=true
) t on t.ref_area = normalize_string(r.TERRITORY_NEXT_RESID)
where cast_int(r.OBS_VALUE) is not null
