-- clean.sql: ASIA imprese e addetti (183_277) — dbnomics CSV lungo
-- Macros toolkit: normalize_string / cast_int / cast_double

select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(REF_AREA) as territorio_codice,
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
    end as territorio,
    case when normalize_string(REF_AREA) = 'IT' then 'italia' else 'nuts1' end as livello,
    normalize_string(ECON_ACTIVITY_NACE_2007) as nace_codice,
    case normalize_string(ECON_ACTIVITY_NACE_2007)
        when '0010' then 'Totale'
        when 'B' then 'Estrazione miniere'
        when 'C' then 'Manifattura'
        when 'D' then 'Energia'
        when 'E' then 'Acqua/rifiuti'
        when 'F' then 'Costruzioni'
        when 'G' then 'Commercio/riparazioni'
        when 'H' then 'Trasporti/magazzinaggio'
        when 'I' then 'Accommodation/food'
        when 'J' then 'Info-communication'
        when 'K' then 'Finanza/assicurazioni'
        when 'L' then 'Immobiliare'
        when 'M' then 'Professional scientific'
        when 'N' then 'Amministrazione/supporto'
        when 'P' then 'Istruzione'
        when 'Q' then 'Salute sociale'
        when 'R' then 'Arte/spettacolo'
        when 'S' then 'Altro servizi'
        else normalize_string(ECON_ACTIVITY_NACE_2007)
    end as nace,
    normalize_string(DATA_TYPE) as indicatore_codice,
    case normalize_string(DATA_TYPE)
        when 'AENTN' then 'Imprese attive'
        when 'AENTEMPDAA' then 'Addetti media annua'
        else normalize_string(DATA_TYPE)
    end as indicatore,
    cast_double(OBS_VALUE) as valore
from raw_input
where cast_int(TIME_PERIOD) is not null
  and normalize_string(DATA_TYPE) in ('AENTN', 'AENTEMPDAA')
  and normalize_string(LEGAL_FORM) = 'TOT'
  and normalize_string(PERS_EMPL_SIZE_CLASS) = 'TOTAL'
  AND cast_double(OBS_VALUE) IS NOT NULL
