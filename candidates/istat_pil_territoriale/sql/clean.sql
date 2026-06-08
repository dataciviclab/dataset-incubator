-- ISTAT SDMX DCCN_PILT — PIL lato offerta
-- Fonte: CSV SDMX da http_file
-- Colonne CSV: DATAFLOW, FREQ, REF_AREA, DATA_TYPE_AGGR, VALUATION, ADJUSTMENT, EDITION, TIME_PERIOD, OBS_VALUE

with
edizione_max as (
    select max(EDITION) as max_ed from raw_input
)
select
    REF_AREA as territorio_codice,
    case
        when REF_AREA = 'IT' then 'nazionale'
        when length(REF_AREA) = 3 then 'macro_area'
        when length(REF_AREA) = 4 and regexp_matches(REF_AREA, 'IT[A-Z][0-9]') then 'regione'
        when length(REF_AREA) = 4 then 'macro_area'
        when length(REF_AREA) = 5 then 'provincia'
        else 'altro'
    end as livello,
    DATA_TYPE_AGGR as tipo_dato_codice,
    VALUATION as valutazione_codice,
    cast(TIME_PERIOD as integer) as anno,
    cast(OBS_VALUE as double) as valore_mln_eu
from raw_input, edizione_max
where EDITION = edizione_max.max_ed
  and VALUATION = 'V'
  and ADJUSTMENT = 'N'
  and OBS_VALUE is not null
