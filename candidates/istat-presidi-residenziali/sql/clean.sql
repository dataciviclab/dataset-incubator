-- clean.sql — ISTAT 49_37 "Presidi residenziali socio-assistenziali e socio-sanitari"
-- Canale SDMX diretto (esploradati). Il container 49_37 restituisce le unita' di
-- servizio (strutture, posti letto, personale) con le 11 dimensioni del DSD
-- DCIS_PRESIDI1. Una riga = area x tipo dato x breakdown x anno.
--
-- Il plugin sdmx scarica l'intera serie: il clean NON filtra per anno, cosi'
-- il parquet del run contiene 2009-2023 e i mart producono la serie completa
-- con un solo fetch (evita il rate-limit ISTAT). Filtriamo i soli DATA_TYPE
-- utili (presidi, posti letto, personale + tassi per 100.000).
-- Le label sono mappate esplicitamente dai codici (codelist ISTAT), cosi' il
-- clean non dipende dalle colonne *_label del payload.

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
        when '70' then 'Presidi residenziali'
        when '72' then 'Presidi residenziali per 100.000 residenti'
        when '73' then 'Posti letto operativi'
        when '75' then 'Posti letto operativi per 100.000 residenti'
        when '76' then 'Personale retribuito'
        when '78' then 'Personale volontario'
        else normalize_string(DATA_TYPE)
    end as tipo_dato,

    normalize_string(MAINLY_TARGET_USERS) as tipo_utenza_codice,
    case normalize_string(MAINLY_TARGET_USERS)
        when 'TOT'    then 'Totale'
        when 'ELD'    then 'Anziani (65+)'
        when 'DIS'    then 'Disabili'
        when 'CHLD'   then 'Minori (0-17)'
        when 'ADUDIS' then 'Adulti con disagio sociale'
        when 'MENT'   then 'Salute mentale'
        when 'ADD'    then 'Dipendenze'
        when 'IMMFOR' then 'Immigrati/stranieri'
        when 'GEND'   then 'Vittime di violenza di genere'
        when 'MULBEN' then 'Multiutenza'
        when 'NRP'    then 'Non indicato'
        else normalize_string(MAINLY_TARGET_USERS)
    end as tipo_utenza,

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

    normalize_string(TYPE_RESID_CARE_CENTRE) as tipo_residenzialita_codice,
    case normalize_string(TYPE_RESID_CARE_CENTRE)
        when 'ALL' then 'Totale'
        when 'ASS' then 'Assistenziale'
        when 'COM' then 'Socio-sanitaria'
        when 'NRP' then 'Non indicato'
        else normalize_string(TYPE_RESID_CARE_CENTRE)
    end as tipo_residenzialita,

    normalize_string(SOCIAL_PROT_FUNCTION) as funzione_protezione_sociale_codice,
    case normalize_string(SOCIAL_PROT_FUNCTION)
        when '15' then 'Accoglienza di emergenza'
        when '16' then 'Prevalente accoglienza abitativa'
        when '17' then 'Prevalente funzione tutelare'
        when '18' then 'Socio-educativa'
        when '19' then 'Educativa psicologica'
        when '20' then 'Socio-sanitaria'
        when '21' then 'Non indicato'
        when '99' then 'Totale'
        else normalize_string(SOCIAL_PROT_FUNCTION)
    end as funzione_protezione_sociale,

    normalize_string(LEGAL_STATUS_OF_HOLDER) as natura_giuridica_codice,
    case normalize_string(LEGAL_STATUS_OF_HOLDER)
        when '1' then 'Pubblico'
        when '2' then 'Non profit'
        when '3' then 'Profit'
        when '4' then 'Privato'
        when '0' then 'Non indicato'
        when '9' then 'Totale'
        else normalize_string(LEGAL_STATUS_OF_HOLDER)
    end as natura_giuridica,

    normalize_string(TYPE_OF_ADMINISTRATOR) as tipo_gestore_codice,
    case normalize_string(TYPE_OF_ADMINISTRATOR)
        when 'TOT'   then 'Totale'
        when '14'    then 'Societa'' cooperativa'
        when '1430'  then 'Societa'' cooperativa sociale'
        when '16'    then 'Ente pubblico economico'
        when '1630'  then 'Azienda pubblica di servizi alle persone'
        when '17'    then 'Ente privato con personalita'' giuridica'
        when '1740'  then 'Ente ecclesiastico'
        when '24'    then 'Regione e autonomia locale'
        when '2410'  then 'Regione'
        when '2420'  then 'Provincia'
        when '2430'  then 'Comune'
        when '25'    then 'Azienda o ente del SSN'
        when 'X1795' then 'Fondazione'
        when 'X2470' then 'Comunita'' montana/unione comuni/citta'' metropolitana'
        when 'X31'   then 'Associazione di volontariato/promozione sociale'
        when 'X32'   then 'Consorzio di cooperative sociali'
        when 'X33'   then 'Societa'' privata'
        when 'X34'   then 'Altro ente pubblico'
        when 'X35'   then 'Altro soggetto privato'
        when 'NSP'   then 'Non indicato'
        else normalize_string(TYPE_OF_ADMINISTRATOR)
    end as tipo_gestore,

    normalize_string(Y_PUBLIC_FUNDING) as finanziamento_pubblico_codice,
    case normalize_string(Y_PUBLIC_FUNDING)
        when '0' then 'No'
        when '1' then 'Si'
        when '2' then 'Non indicato'
        when '9' then 'Totale'
        else normalize_string(Y_PUBLIC_FUNDING)
    end as finanziamento_pubblico,

    normalize_string(PROF_STATUS) as professione_codice,
    case normalize_string(PROF_STATUS)
        when 'ALL'      then 'Totale'
        when 'ACTLEA'   then 'Animatori'
        when 'CIVSER'   then 'Servizio civile'
        when 'CULMED'   then 'Mediatori culturali'
        when 'DIRCRD'   then 'Direttori e dirigenti'
        when 'EMPL'     then 'Impiegati'
        when 'GENSER'   then 'Altri addetti servizi generali'
        when 'HEAWOR'   then 'Assistenti sanitari'
        when 'NURS'     then 'Infermieri'
        when 'OTHQUAL'  then 'Altro personale'
        when 'PARFIG'   then 'Figure genitoriali'
        when 'PERSCARE' then 'Altri addetti assistenza alla persona'
        when 'PHYS'     then 'Fisioterapisti'
        when 'PRACT'    then 'Medici di medicina generale'
        when 'PREFOOD'  then 'Addetto preparazione e distribuzione cibo'
        when 'PROFYWOR' then 'Educatori professionali'
        when 'PSY'      then 'Psicologi'
        when 'REHPHYS'  then 'Terapisti riabilitazione'
        when 'SOC'      then 'Sociologi'
        when 'SOCWOR'   then 'Assistenti sociali'
        when 'SPECDOCT' then 'Specialisti in terapie mediche'
        when 'SPETHE'   then 'Logopedisti'
        when 'TEACH'    then 'Insegnanti nella formazione professionale'
        else normalize_string(PROF_STATUS)
    end as professione,

    cast_double(value) as valore
from raw_input
where normalize_string(FREQ) = 'A'
  and normalize_string(DATA_TYPE) in ('70', '72', '73', '75', '76', '78')
  and cast_double(value) is not null
