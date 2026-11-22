-- clean.sql: censimento permanente abitazioni — tavole comunali SDMX
-- Fonti (stesso schema):
--   DF_DCSS_ABITAZIONI_TV_1  stock / occupate / non occupate      (2019, 2021, 2023)
--   DF_DCSS_ABITAZIONI_TV_2  occupate per titolo di possesso      (2019, 2021, 2023)
--
-- Solo il 2021 e' enumerazione completa: 2019 e 2023 sono edizioni campionarie.
--
-- all_varchar: true -> i codici con zeri iniziali sopravvivono; i cast sono qui.

with base as (
    select
        cast_int(TIME_PERIOD) as anno,
        normalize_string(REF_AREA) as territorio_codice,
        normalize_string(INDICATOR) as misura_codice,
        normalize_string(OWNERSHIP_TYPE) as titolo_possesso_codice,
        cast_double(OBS_VALUE) as valore
    from raw_input
)

select distinct
    anno,
    territorio_codice,
    -- IT=2, ripartizioni=3, regioni=4, province=5, comuni=6
    case length(territorio_codice)
        when 2 then 'italia'
        when 3 then 'ripartizione'
        when 4 then 'regione'
        when 5 then 'provincia'
        when 6 then 'comune'
        else 'altro'
    end as livello_geografico,
    misura_codice,
    case misura_codice
        when 'NUM_DW_AV' then 'abitazioni'
        when 'NUM_OCC_DW_AV' then 'abitazioni occupate'
        when 'NUM_UNOCC_DW_AV' then 'abitazioni non occupate'
    end as misura,
    titolo_possesso_codice,
    case titolo_possesso_codice
        when 'ALL' then 'tutte le voci'
        when 'OWN' then 'proprietà'
        when 'RENT' then 'affitto'
        when 'OTH_OR' then 'altro titolo diverso da proprietà, affitto'
    end as titolo_possesso,
    valore
from base
-- distinct sopra: TV_1 e TV_2 espongono entrambi la riga di totale (ALL),
-- che altrimenti verrebbe duplicata nel join dei due raw
where anno is not null
  and territorio_codice is not null
  and misura_codice is not null
  and valore is not null
order by anno, territorio_codice, misura_codice, titolo_possesso_codice
