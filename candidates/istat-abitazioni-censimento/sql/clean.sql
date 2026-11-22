-- clean.sql: censimento permanente abitazioni — bulk comunale ISTAT
-- Fonte: DWL/PERMPOP/MUN/DCSS_ABITAZIONI (zip -> csv pipe-delimited, UTF-8 con BOM)
--
-- 2021 = enumerazione completa: totale / occupate / non occupate, per comune
-- 2019 = edizione campionaria: occupate per titolo di possesso, valori decimali
--        (stima, non conteggio) e senza totale abitazioni a livello comunale
--
-- all_varchar: true in dataset.yml -> tutti i campi arrivano come stringhe:
-- i codici con zeri iniziali (ITTER107 = 001001) sopravvivono allo sniffing.

with base as (
    select
        cast_int("Seleziona periodo") as anno,
        normalize_string(ITTER107) as territorio_codice,
        normalize_string(Territorio) as territorio,
        normalize_string(TIPO_DATO_CENS_POP) as misura_codice,
        normalize_string("Tipo dato") as misura,
        normalize_string(TIT_POSSESSO) as titolo_possesso_codice,
        normalize_string("Tipo di possesso") as titolo_possesso,
        normalize_string(NUMEROSITA) as stanze_codice,
        normalize_string("Numero di stanze") as stanze,
        normalize_string(SUPERFICIE) as superficie_codice,
        normalize_string("Classi di superficie") as superficie,
        normalize_string(EDIFICI_A) as accessibilita_codice,
        normalize_string(EDIFICI_B) as tipo_edificio_codice,
        cast_double(Value) as valore
    from raw_input
)

select
    anno,
    territorio_codice,
    territorio,
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
    misura,
    titolo_possesso_codice,
    titolo_possesso,
    stanze_codice,
    stanze,
    superficie_codice,
    superficie,
    accessibilita_codice,
    tipo_edificio_codice,
    valore
from base
where anno is not null
  and territorio_codice is not null
  and misura_codice is not null
  and valore is not null
order by anno, territorio_codice, misura_codice
