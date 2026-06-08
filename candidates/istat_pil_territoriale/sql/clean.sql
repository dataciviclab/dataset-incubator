-- ISTAT SDMX DCCN_PILT — PIL lato offerta
-- Fonte: SDMX (JSON -> CSV con _label columns)
-- Colonne raw: FREQ, FREQ_label, REF_AREA, REF_AREA_label,
--   DATA_TYPE_AGGR, DATA_TYPE_AGGR_label, VALUATION, VALUATION_label,
--   ADJUSTMENT, ADJUSTMENT_label, EDITION, EDITION_label,
--   TIME_PERIOD, TIME_PERIOD_label, value

with
edizione_max as (
    select max(EDITION) as max_ed from raw_input
)
select
    REF_AREA as territorio_codice,
    REF_AREA_label as territorio_nome,
    case
        when REF_AREA = 'IT' then 'nazionale'
        when length(REF_AREA) = 3 then 'macro_area'
        when length(REF_AREA) = 4 and REF_AREA not similar to 'IT[A-Z]{2,}' then 'regione'
        when length(REF_AREA) = 4 then 'macro_area'
        when length(REF_AREA) = 5 and REF_AREA not similar to 'IT[A-Z]{2,}' then 'provincia'
        else 'altro'
    end as livello,
    DATA_TYPE_AGGR as tipo_dato_codice,
    DATA_TYPE_AGGR_label as tipo_dato,
    VALUATION as valutazione_codice,
    VALUATION_label as valutazione,
    cast(TIME_PERIOD as integer) as anno,
    cast(value as double) as valore_mln_eu
from raw_input, edizione_max
where EDITION = edizione_max.max_ed
  and VALUATION = 'V'
  and ADJUSTMENT = 'N'
  and value is not null
