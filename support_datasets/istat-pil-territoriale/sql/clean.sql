-- ISTAT 93_498 — PIL/VA/imposte lato offerta
-- Canale dbnomics · macros toolkit (normalize_string / cast_int / cast_double)
-- Ultima edizione per REF_AREA × DATA_TYPE_AGGR

with
edizione_max as (
    select
        normalize_string(REF_AREA) as REF_AREA,
        normalize_string(DATA_TYPE_AGGR) as DATA_TYPE_AGGR,
        max(normalize_string(EDITION)) as max_ed
    from raw_input
    group by 1, 2
)
select
    normalize_string(r.REF_AREA) as territorio_codice,
    case normalize_string(r.REF_AREA)
        when 'IT' then 'Italia'
        else normalize_string(r.REF_AREA)
    end as territorio_nome,
    case
        when normalize_string(r.REF_AREA) = 'IT' then 'nazionale'
        when length(normalize_string(r.REF_AREA)) = 3 then 'macro_area'
        when length(normalize_string(r.REF_AREA)) = 4
             and normalize_string(r.REF_AREA) not similar to 'IT[A-Z]{2,}' then 'regione'
        when length(normalize_string(r.REF_AREA)) = 4 then 'macro_area'
        when length(normalize_string(r.REF_AREA)) = 5
             and normalize_string(r.REF_AREA) not similar to 'IT[A-Z]{2,}' then 'provincia'
        else 'altro'
    end as livello,
    normalize_string(r.DATA_TYPE_AGGR) as tipo_dato_codice,
    case normalize_string(r.DATA_TYPE_AGGR)
        when 'B1GQ_B_W2_S1' then 'PIL'
        when 'B1G_B_W2_S1' then 'VA'
        when 'D21X31_C_W2_S1' then 'Imposte nette prodotti'
        else normalize_string(r.DATA_TYPE_AGGR)
    end as tipo_dato,
    normalize_string(r.VALUATION) as valutazione_codice,
    'prezzi correnti' as valutazione,
    cast_int(r.TIME_PERIOD) as anno,
    cast_double(r.OBS_VALUE) as valore_mln_eu
from raw_input r
join edizione_max e
  on normalize_string(r.REF_AREA) = e.REF_AREA
 and normalize_string(r.DATA_TYPE_AGGR) = e.DATA_TYPE_AGGR
 and normalize_string(r.EDITION) = e.max_ed
where normalize_string(r.VALUATION) = 'V'
  and normalize_string(r.ADJUSTMENT) = 'N'
  and anno is not null
  and valore_mln_eu is not null
