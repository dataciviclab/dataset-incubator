-- clean.sql: stranieri residenti al 1 gennaio per provincia x cittadinanza
-- (ISTAT 29_317_DF_DCIS_POPSTRCIT1_1 via DBnomics)
--
-- Grano: anno x territorio (nazionale/ripartizione/regione/provincia) x
-- cittadinanza. Nomi da codelist locali (estratte dal metadata DBnomics).

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.REF_AREA) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    normalize_string(r.CITIZENSHIP) as cittadinanza_codice,
    c.nome as cittadinanza,
    cast_int(r.OBS_VALUE) as residenti
from raw_input r
left join read_csv(
    'candidates/istat-stranieri-residenti/codelists/istat_territori.csv',
    auto_detect=true, header=true
) t on t.ref_area = normalize_string(r.REF_AREA)
left join read_csv(
    'candidates/istat-stranieri-residenti/codelists/istat_cittadinanze.csv',
    auto_detect=true, header=true
) c on c.codice = normalize_string(r.CITIZENSHIP)
where cast_int(r.OBS_VALUE) is not null
