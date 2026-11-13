-- clean.sql — ISTAT 49_62 "Ospiti dei presidi residenziali
-- socio-assistenziali e socio-sanitari"
-- Canale DBnomics (mirror ISTAT). Output plugin: una riga = serie x anno,
-- colonne = dimensioni DSD + TIME_PERIOD + OBS_VALUE.
--
-- Il clean non filtra per anno: il parquet del run contiene 2009-2023.
-- Tiene solo il perimetro v0 (ospiti totali, anziani 65+, stranieri) e fissa
-- le dimensioni non usate ai totali. Per i dati adulti/anziani le dimensioni
-- "minori" valgono NAP (non ALL): entrambe ammesse.

select
    cast_int(TIME_PERIOD) as anno,

    normalize_string(REF_AREA) as ref_area_codice,
    case normalize_string(REF_AREA)
        when 'IT'    then 'Italia'
        when 'ITC'   then 'Nord-ovest'
        when 'ITD'   then 'Nord-est'
        when 'ITE'   then 'Centro'
        when 'ITF'   then 'Sud'
        when 'ITG'   then 'Isole'
        when 'ITDA'  then 'Trentino-Alto Adige'
        when 'ITC1'  then 'Piemonte'
        when 'ITC2'  then 'Valle d''Aosta/Vallée d''Aoste'
        when 'ITC3'  then 'Liguria'
        when 'ITC4'  then 'Lombardia'
        when 'ITD1'  then 'Bolzano/Bozen'
        when 'ITD2'  then 'Trento'
        when 'ITD3'  then 'Veneto'
        when 'ITD4'  then 'Friuli-Venezia Giulia'
        when 'ITD5'  then 'Emilia-Romagna'
        when 'ITE1'  then 'Toscana'
        when 'ITE2'  then 'Umbria'
        when 'ITE3'  then 'Marche'
        when 'ITE4'  then 'Lazio'
        when 'ITF1'  then 'Abruzzo'
        when 'ITF2'  then 'Molise'
        when 'ITF3'  then 'Campania'
        when 'ITF4'  then 'Puglia'
        when 'ITF5'  then 'Basilicata'
        when 'ITF6'  then 'Calabria'
        when 'ITG1'  then 'Sicilia'
        when 'ITG2'  then 'Sardegna'
        else normalize_string(REF_AREA)
    end as regione,

    normalize_string(DATA_TYPE) as tipo_dato_codice,
    case normalize_string(DATA_TYPE)
        when '80' then 'Ospiti'
        when '89' then 'Anziani 65+'
        when '92' then 'Stranieri'
        else normalize_string(DATA_TYPE)
    end as tipo_dato,

    normalize_string(AGE) as eta_codice,
    case normalize_string(AGE)
        when 'TOTAL'  then 'Totale'
        when 'Y_GE65' then '65 anni e oltre'
        else normalize_string(AGE)
    end as eta,

    normalize_string(NEED_TYPE) as bisogno_codice,
    case normalize_string(NEED_TYPE)
        when 'ALL'         then 'Totale'
        when 'SELSUFELD'   then 'Autosufficienti'
        when 'NOSELSUFELD' then 'Non autosufficienti'
        else normalize_string(NEED_TYPE)
    end as bisogno,

    normalize_string(HEALTHCARE_LEVEL) as livello_assistenza_codice,
    case normalize_string(HEALTHCARE_LEVEL)
        when 'ALL'  then 'Totale'
        when 'ABS'  then 'Assente'
        when 'LOW'  then 'Basso'
        when 'MED'  then 'Medio'
        when 'HIGH' then 'Alto'
        when 'NSP'  then 'Non indicato'
        else normalize_string(HEALTHCARE_LEVEL)
    end as livello_assistenza,

    cast_int(OBS_VALUE) as ospiti
from raw_input
where normalize_string(FREQ) = 'A'
  and normalize_string(DATA_TYPE) in ('80', '89', '92')
  and normalize_string(AGE) in ('TOTAL', 'Y_GE65')
  and normalize_string(SEX) = '9'
  and normalize_string(NEED_TYPE) in ('ALL', 'SELSUFELD', 'NOSELSUFELD')
  and normalize_string(HEALTHCARE_LEVEL) in ('ALL', 'ABS', 'LOW', 'MED', 'HIGH')
  and normalize_string(SOCIAL_PROT_FUNCTION) = '99'
  and normalize_string(TYPE_RESID_CARE_CENTRE) = 'ALL'
  and normalize_string(REASON_ADMISSION_MINOR) in ('ALL', 'NAP')
  and normalize_string(ORIG_MINOR_GUESTS) in ('ALL', 'NAP')
  and normalize_string(ADOPTAB_STATUS_MINOR) in ('ALL', 'NAP')
  and normalize_string(DEST_MINOR_GUESTS) in ('ALL', 'NAP')
  and cast_int(OBS_VALUE) is not null
