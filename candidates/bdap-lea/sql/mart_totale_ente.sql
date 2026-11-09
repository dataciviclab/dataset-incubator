-- Totale pubblicato per ente e anno, con la sua composizione.
-- 49999 è l'unico totale affidabile: NON derivarlo dalla somma delle voci di
-- dettaglio, che sono gerarchiche (genitore + figli) e gonfiano il risultato.
-- Identità verificata: 49999 = 19999 + 29999 + 39999 + 48888 su 217/217 enti.
with voci as (
    select
        anno_riferimento,
        codice_regione,
        any_value(descrizione_regione) as descrizione_regione,
        codice_ente_bdap,
        codice_ente_ssn,
        any_value(descrizione_ente) as descrizione_ente,
        sum(case when codice_voce_contabile = '49999' then importo_totale end) as totale,
        sum(case when codice_voce_contabile = '19999' then importo_totale end) as prevenzione,
        sum(case when codice_voce_contabile = '29999' then importo_totale end) as distrettuale,
        sum(case when codice_voce_contabile = '39999' then importo_totale end) as ospedaliera,
        sum(case when codice_voce_contabile = '48888' then importo_totale end) as ricerca
    from clean_input
    where tipo_voce = 'totale'
      and tipo_riga = 'ente'
    group by anno_riferimento, codice_regione, codice_ente_bdap, codice_ente_ssn
)

select
    *,
    coalesce(prevenzione, 0)
        + coalesce(distrettuale, 0)
        + coalesce(ospedaliera, 0)
        + coalesce(ricerca, 0) as totale_calcolato,
    round(
        coalesce(prevenzione, 0)
        + coalesce(distrettuale, 0)
        + coalesce(ospedaliera, 0)
        + coalesce(ricerca, 0)
        - coalesce(totale, 0),
        2
    ) as quadratura,
    round(coalesce(prevenzione, 0) / nullif(totale, 0), 4) as quota_prevenzione,
    round(coalesce(distrettuale, 0) / nullif(totale, 0), 4) as quota_distrettuale,
    round(coalesce(ospedaliera, 0) / nullif(totale, 0), 4) as quota_ospedaliera
from voci
