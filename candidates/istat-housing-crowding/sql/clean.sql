-- clean.sql: crowding index 33_179
-- Canale SDMX diretto (esploradati) · macros toolkit (normalize_string / cast_int / cast_double)
-- Raw contiene anche le breakdown (dimensioni non filtrate, key vuota = all,
-- fix toolkit #444). Nota: ISTAT espone le breakdown SOLO sul totale delle
-- famiglie (TENURE_STATUS=99); rent/property esistono solo come totali.
-- TENURE_STATUS secondo le label ISTAT: 1=rent (Affitto), 2=property (Proprietà).

select
    cast_int(TIME_PERIOD) as anno,
    normalize_string(REF_AREA) as ref_area_codice,
    case normalize_string(REF_AREA)
        when 'IT' then 'Italia'
        else normalize_string(REF_AREA)
    end as ref_area,
    normalize_string(DATA_TYPE) as indicatore_codice,
    DATA_TYPE_label as indicatore,
    normalize_string(MEASURE) as misura_codice,
    MEASURE_label as misura,
    normalize_string(TENURE_STATUS) as titolo_godimento_codice,
    case normalize_string(TENURE_STATUS)
        when '1' then 'Affitto'
        when '2' then 'Proprietà'
        when '99' then 'Totale famiglie'
        else TENURE_STATUS_label
    end as titolo_godimento,
    cast_int(NUMBER_HOUSEHOLD_COMP) as numero_componenti_nucleo,
    NUMBER_HOUSEHOLD_COMP_label as numero_componenti_nucleo_label,
    normalize_string(HOUSEHOLD_TYPOLOGY) as tipologia_nucleo_codice,
    HOUSEHOLD_TYPOLOGY_label as tipologia_nucleo_label,
    cast_int(NUMB_OF_CHILDREN) as numero_figli,
    NUMB_OF_CHILDREN_label as numero_figli_label,
    cast_int(NUMB_OF_ELDERLY) as numero_anziani,
    NUMB_OF_ELDERLY_label as numero_anziani_label,
    normalize_string(FIFTH_EQUIV_HOUSE_INC) as quintile_reddito_codice,
    FIFTH_EQUIV_HOUSE_INC_label as quintile_reddito_label,
    normalize_string(SEX_MAIN_PERCEPTOR) as sesso_percettore_principale_codice,
    SEX_MAIN_PERCEPTOR_label as sesso_percettore_principale_label,
    normalize_string(AGE_MAIN_EARNIER) as eta_percettore_principale_codice,
    AGE_MAIN_EARNIER_label as eta_percettore_principale_label,
    normalize_string(EDU_LEV_MAIN_EARN) as titolo_studio_percettore_codice,
    EDU_LEV_MAIN_EARN_label as titolo_studio_percettore_label,
    normalize_string(LABPROF_STATUS_C_MAIN_EARNER) as condizione_professionale_percettore_codice,
    LABPROF_STATUS_C_MAIN_EARNER_label as condizione_professionale_percettore_label,
    cast_double(value) as componenti_per_100mq
from raw_input
where cast_int(TIME_PERIOD) is not null
  and normalize_string(DATA_TYPE) = 'ABITAZ_AFFOLL_MED'
  and normalize_string(TENURE_STATUS) in ('1', '2', '99')
  and cast_double(value) is not null
