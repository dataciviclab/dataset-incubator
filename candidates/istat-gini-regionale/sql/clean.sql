-- clean.sql: Gini reddito netto regionale (32_221)
-- Canale dbnomics · macros toolkit (normalize_string / cast_int / cast_double)

select
    normalize_string(REF_AREA) as regione_codice,
    case normalize_string(REF_AREA)
        when 'IT' then 'Italia'
        when 'ITC1' then 'Piemonte'
        when 'ITC2' then 'Valle d''Aosta'
        when 'ITC3' then 'Liguria'
        when 'ITC4' then 'Lombardia'
        when 'ITD1' then 'Provincia Autonoma Bolzano'
        when 'ITD2' then 'Provincia Autonoma Trento'
        when 'ITD3' then 'Veneto'
        when 'ITD4' then 'Friuli-Venezia Giulia'
        when 'ITD5' then 'Emilia-Romagna'
        when 'ITE1' then 'Toscana'
        when 'ITE2' then 'Umbria'
        when 'ITE3' then 'Marche'
        when 'ITE4' then 'Lazio'
        when 'ITF1' then 'Abruzzo'
        when 'ITF2' then 'Molise'
        when 'ITF3' then 'Campania'
        when 'ITF4' then 'Puglia'
        when 'ITF5' then 'Basilicata'
        when 'ITF6' then 'Calabria'
        when 'ITG1' then 'Sicilia'
        when 'ITG2' then 'Sardegna'
        else normalize_string(REF_AREA)
    end as regione,
    normalize_string(DATA_TYPE) as tipo_dato,
    normalize_string(IMPUTED_RENTS) as pres_aff_imp,
    cast_int(TIME_PERIOD) as anno,
    cast_double(OBS_VALUE) as gini
from raw_input
where normalize_string(DATA_TYPE) = 'DISUG_REDDNET_GINI'
  and normalize_string(IMPUTED_RENTS) in ('1', '2')
  and length(normalize_string(REF_AREA)) = 4
  and gini is not null
