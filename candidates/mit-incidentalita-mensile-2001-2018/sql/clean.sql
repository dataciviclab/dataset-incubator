-- clean.sql — mit-incidentalita-mensile-2001-2018
--
-- Perimetro: solo righe mensili (216 righe su 288 totali).
-- Le 72 righe trimestrali ("1° Trimestre", ecc.) sono escluse perché
-- la fonte MIT presenta anomalie non recuperabili su ~13 trimestri:
-- trailing zero mancante e valori irregolari.
--
-- Note tecniche:
-- - il file raw è utf-8 con BOM: si legge con header:false + skip:1
--   e colonne esplicite (evita problemi di nome colonna con BOM)
-- - i campi percentuale/indice usano la virgola come decimale nel raw
--   (valori quoted): REPLACE(',', '.') + CAST AS DOUBLE
-- - il campo mese_raw ha leading spaces nel raw: TRIM
-- - alcune righe trimestrali tardive hanno colonne in eccesso (null_padding)

with base as (
    select
        trim(mese_raw)                                          as mese,
        cast(trim(anno_raw) as integer)                        as anno,
        cast(nullif(trim(incidenti_raw), '') as integer)       as incidenti,
        cast(nullif(trim(morti_raw), '') as integer)           as morti,
        cast(nullif(trim(feriti_raw), '') as integer)          as feriti,
        cast(nullif(trim(incidenti_mortali_raw), '') as integer) as incidenti_mortali,
        cast(replace(nullif(trim(perc_incidenti_raw), ''), ',', '.') as double)           as perc_incidenti,
        cast(replace(nullif(trim(perc_incidenti_mortali_raw), ''), ',', '.') as double)   as perc_incidenti_mortali,
        cast(replace(nullif(trim(perc_morti_raw), ''), ',', '.') as double)               as perc_morti,
        cast(replace(nullif(trim(perc_feriti_raw), ''), ',', '.') as double)              as perc_feriti,
        cast(replace(nullif(trim(indice_mortalita_raw), ''), ',', '.') as double)         as indice_mortalita,
        cast(replace(nullif(trim(indice_gravita_raw), ''), ',', '.') as double)           as indice_gravita,
        cast(replace(nullif(trim(indice_lesivita_raw), ''), ',', '.') as double)          as indice_lesivita,
        cast(replace(nullif(trim(indice_mortalita_spec_raw), ''), ',', '.') as double)    as indice_mortalita_spec,
        cast(replace(nullif(trim(indice_incidentalita_spec_raw), ''), ',', '.') as double) as indice_incidentalita_spec
    from raw_input
),
mensili as (
    select *
    from base
    where mese in (
        'Gennaio', 'Febbraio', 'Marzo', 'Aprile',
        'Maggio', 'Giugno', 'Luglio', 'Agosto',
        'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
    )
)
select
    *,
    case mese
        when 'Gennaio'   then 1  when 'Febbraio'  then 2
        when 'Marzo'     then 3  when 'Aprile'    then 4
        when 'Maggio'    then 5  when 'Giugno'    then 6
        when 'Luglio'    then 7  when 'Agosto'    then 8
        when 'Settembre' then 9  when 'Ottobre'   then 10
        when 'Novembre'  then 11 when 'Dicembre'  then 12
    end as mese_numero
from mensili
order by anno, mese_numero
