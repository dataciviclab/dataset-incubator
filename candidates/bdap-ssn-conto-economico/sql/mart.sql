-- Composizione regionale del Conto Economico SSN: una riga per anno e regione.
-- Le voci sono selezionate per codice (AA0010, BA2090, ...), che è stabile
-- 2012-2024; la numerazione nella descrizione (B.10 vs B.16) invece cambia.
-- I totali di sezione sono i codici *Z9999 (AZ9999, BZ9999, ZZ9999).
with voci as (
    select
        anno,
        codice_regione,
        descrizione_regione,
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
    group by anno, codice_regione, descrizione_regione
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
    -- quote per lettura civica: quanto del costo se ne va in personale,
    -- quanto dei ricavi arriva dal finanziamento indistinto
    round(costo_personale / nullif(totale_costi, 0), 4) as quota_personale_su_costi,
    round(contributi_esercizio / nullif(totale_ricavi, 0), 4) as quota_contributi_su_ricavi
from composizione
