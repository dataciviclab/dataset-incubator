-- clean.sql: acquisizioni di cittadinanza italiana (ISTAT 29_849 via DBnomics)
--
-- Grano: anno x territorio (nazionale/ripartizione/regione/provincia) x
-- ex-cittadinanza x processo di acquisizione.
-- I nomi di territori e cittadinanze vengono da codelist locali (estratte dal
-- metadata DBnomics), per non dipendere da label hardcoded nel SQL.

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.REF_AREA) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    normalize_string(r.MOSTREL_CCITENSHIP) as cittadinanza_codice,
    c.nome as cittadinanza,
    normalize_string(r.ACQUISITION_PROCESS) as processo_codice,
    case normalize_string(r.ACQUISITION_PROCESS)
        when 'ALL' then 'Totale'
        when 'MAT' then 'Matrimonio'
        when 'RS' then 'Residenza'
        when 'TRS' then 'Altro'
        else normalize_string(r.ACQUISITION_PROCESS)
    end as processo,
    cast_int(r.OBS_VALUE) as acquisizioni
from raw_input r
left join read_csv(
    'candidates/istat-cittadinanze/codelists/istat_territori.csv',
    auto_detect=true, header=true
) t on t.ref_area = normalize_string(r.REF_AREA)
left join read_csv(
    'candidates/istat-cittadinanze/codelists/istat_cittadinanze.csv',
    auto_detect=true, header=true
) c on c.codice = normalize_string(r.MOSTREL_CCITENSHIP)
where cast_int(r.OBS_VALUE) is not null
