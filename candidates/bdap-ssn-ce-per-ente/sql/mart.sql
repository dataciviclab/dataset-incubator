-- Conto Economico per singola azienda sanitaria, con le righe di consolidamento.
--
-- `tipo_riga`:
--   ente        azienda sanitaria (da sommare tra loro)
--   regione     ente regione (000): soggetto reale, NON un aggregato
--   consolidato totale regionale (999): uguale al dataset CE regionale
--
-- ATTENZIONE: a differenza dello Stato Patrimoniale, qui **ricavi e costi non
-- sono additivi**. Le aziende si scambiano prestazioni e ricevono trasferimenti
-- dalla regione: il consolidato elimina quei flussi. Nel 2024 la somma dei
-- ricavi degli enti (170,3 mld) è maggiore del consolidato (150,1 mld)di ~20 mld.
-- Il **risultato** invece quadra (000 + enti ≈ 999).
with voci as (
    select
        anno,
        codice_regione,
        any_value(descrizione_regione) as descrizione_regione,
        codice_ente_bdap,
        codice_ente_ssn,
        any_value(descrizione_ente) as descrizione_ente,
        any_value(tipo_riga) as tipo_riga,
        sum(case when codice_voce = 'AA0010' then importo end) as contributi_esercizio,
        sum(case when codice_voce = 'AA0320' then importo end) as ricavi_prestazioni,
        sum(case when codice_voce = 'AA0940' then importo end) as ticket,
        sum(case when codice_voce = 'AZ9999' then importo end) as totale_ricavi,
        sum(case when codice_voce = 'BA0010' then importo end) as acquisti_beni,
        sum(case when codice_voce = 'BA0390' then importo end) as acquisti_servizi,
        sum(case when codice_voce = 'BA1910' then importo end) as manutenzione,
        sum(case when codice_voce = 'BA1990' then importo end) as godimento_beni_terzi,
        sum(case when codice_voce = 'BA2090' then importo end) as personale_sanitario,
        sum(case when codice_voce = 'BA2230' then importo end) as personale_professionale,
        sum(case when codice_voce = 'BA2320' then importo end) as personale_tecnico,
        sum(case when codice_voce = 'BA2410' then importo end) as personale_amministrativo,
        sum(case when codice_voce = 'BA2500' then importo end) as oneri_diversi,
        sum(case when codice_voce = 'BZ9999' then importo end) as totale_costi,
        sum(case when codice_voce = 'ZZ9999' then importo end) as risultato_esercizio
    from clean_input
    group by anno, codice_regione, codice_ente_bdap, codice_ente_ssn
),

composizione as (
    select
        *,
        coalesce(personale_sanitario, 0)
            + coalesce(personale_professionale, 0)
            + coalesce(personale_tecnico, 0)
            + coalesce(personale_amministrativo, 0) as costo_personale
    from voci
)

select
    anno,
    codice_regione,
    descrizione_regione,
    codice_ente_bdap,
    codice_ente_ssn,
    descrizione_ente,
    tipo_riga,
    contributi_esercizio,
    ricavi_prestazioni,
    ticket,
    totale_ricavi,
    acquisti_beni,
    acquisti_servizi,
    manutenzione,
    godimento_beni_terzi,
    personale_sanitario,
    personale_professionale,
    personale_tecnico,
    personale_amministrativo,
    costo_personale,
    oneri_diversi,
    totale_costi,
    risultato_esercizio,
    round(costo_personale / nullif(totale_costi, 0), 4) as quota_personale_su_costi,
    round(contributi_esercizio / nullif(totale_ricavi, 0), 4) as quota_contributi_su_ricavi
from composizione
