-- clean.sql: edilizia residenziale pubblica — interventi finanziati (MIT, DL 47/2014)
-- Fonte: interventiediliziapubblica.csv, snapshot aggiornato ogni 6 ore dalla fonte.
--
-- Trappola del tracciato: `Descrizione` contiene il NOME DEL COMUNE (es. "Abano Terme"),
-- non la descrizione dell'intervento. Mappato su `comune`.
-- Date ISO (YYYY-MM-DD), importi con punto decimale, codici ISTAT con zeri iniziali:
-- all_varchar e' obbligatorio, i cast sono qui.

with base as (
    select
        normalize_string(Codice) as codice_intervento,
        safe_date(PeriodoMonitoraggio) as periodo_monitoraggio,
        normalize_string(Annualita) as annualita_programma,
        normalize_string(LineaIntervento) as linea_intervento,
        normalize_string(Attuatore) as attuatore,
        normalize_string(TipoAttuatore) as tipo_attuatore,
        normalize_string(Stato) as stato,
        normalize_string(ComuneID) as codice_catastale,
        normalize_string(Descrizione) as comune,
        normalize_string(CodiceIstat) as codice_istat_comune,
        normalize_string(Provincia) as provincia,
        normalize_string(Regione) as regione,
        normalize_string(Localizzazione) as localizzazione,
        cast_double(ImportoIntervento) as importo_intervento,
        cast_int(NumeroAlloggi) as numero_alloggi,
        safe_date(LavoriIniziatiData) as data_inizio_lavori,
        safe_date(LavoriUltimatiData) as data_fine_lavori,
        -- -1 e' un sentinella amministrativo per "non dichiarato" (48 interventi
        -- su assegnati, 1 su sfratto): un conteggio negativo non esiste, quindi
        -- diventa NULL invece di essere sommato o interpretato come zero
        case when cast_int(AlloggiAssegnatiNumero) < 0 then null
             else cast_int(AlloggiAssegnatiNumero) end as alloggi_assegnati,
        case when cast_int(AlloggiSfrattoNumero) < 0 then null
             else cast_int(AlloggiSfrattoNumero) end as alloggi_sfratto
    from raw_input
)

select
    codice_intervento,
    periodo_monitoraggio,
    annualita_programma,
    linea_intervento,
    attuatore,
    tipo_attuatore,
    stato,
    codice_catastale,
    comune,
    codice_istat_comune,
    provincia,
    regione,
    localizzazione,
    importo_intervento,
    numero_alloggi,
    data_inizio_lavori,
    data_fine_lavori,
    -- 5 interventi hanno data di fine lavori precedente alla data di inizio:
    -- l'anomalia viene esposta con un flag e la durata resta NULL, invece di
    -- produrre una durata negativa o di scartare la riga in silenzio
    (data_inizio_lavori is not null
        and data_fine_lavori is not null
        and data_fine_lavori < data_inizio_lavori) as date_incoerenti,
    case
        when data_inizio_lavori is not null
             and data_fine_lavori is not null
             and data_fine_lavori >= data_inizio_lavori
        then date_diff('day', data_inizio_lavori, data_fine_lavori)
    end as durata_lavori_giorni,
    alloggi_assegnati,
    alloggi_sfratto
from base
where codice_intervento is not null
order by codice_intervento
