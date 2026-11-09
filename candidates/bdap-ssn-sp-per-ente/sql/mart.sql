-- Patrimonio per singola azienda sanitaria, con le righe di consolidamento.
--
-- `tipo_riga` distingue:
--   ente        azienda sanitaria (da sommare tra loro)
--   regione     ente regione (000): soggetto reale, NON un aggregato
--   consolidato totale regionale (999): uguale al totale della famiglia
--               regionale, NON va sommato agli altri
-- La convenzione 000/999 è invertita rispetto al modello LEA: qui 000 è
-- l'ente regione e 999 il consolidato.
--
-- I totali generali pubblicati mancano in molte righe: attivo e passivo sono
-- derivati dai totali di sezione, come nel dataset regionale.
with voci as (
    select
        anno,
        codice_regione,
        any_value(descrizione_regione) as descrizione_regione,
        codice_ente_bdap,
        codice_ente_ssn,
        any_value(descrizione_ente) as descrizione_ente,
        any_value(tipo_riga) as tipo_riga,
        sum(case when codice_voce = 'AAZ999' then importo end) as immobilizzazioni,
        sum(case when codice_voce = 'ABZ999' then importo end) as attivo_circolante,
        sum(case when codice_voce = 'ACZ999' then importo end) as ratei_attivi,
        sum(case when codice_voce = 'PAZ999' then importo end) as patrimonio_netto,
        sum(case when codice_voce = 'PBZ999' then importo end) as fondi_rischi,
        sum(case when codice_voce = 'PCZ999' then importo end) as tfr,
        sum(case when codice_voce = 'PDZ999' then importo end) as debiti,
        sum(case when codice_voce = 'PEZ999' then importo end) as ratei_passivi,
        sum(case when codice_voce = 'PAA220' then importo end) as utile_esercizio,
        sum(case when codice_voce = 'AZZ999' then importo end) as attivo_pubblicato,
        sum(case when codice_voce = 'PZZ999' then importo end) as passivo_pubblicato
    from clean_input
    group by anno, codice_regione, codice_ente_bdap, codice_ente_ssn
),

totali as (
    select
        *,
        coalesce(immobilizzazioni, 0)
            + coalesce(attivo_circolante, 0)
            + coalesce(ratei_attivi, 0) as attivo,
        coalesce(patrimonio_netto, 0)
            + coalesce(fondi_rischi, 0)
            + coalesce(tfr, 0)
            + coalesce(debiti, 0)
            + coalesce(ratei_passivi, 0) as passivo
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
    immobilizzazioni,
    attivo_circolante,
    ratei_attivi,
    attivo,
    patrimonio_netto,
    fondi_rischi,
    tfr,
    debiti,
    ratei_passivi,
    passivo,
    utile_esercizio,
    round(attivo - passivo, 2) as quadratura,
    attivo_pubblicato,
    passivo_pubblicato,
    round(debiti / nullif(attivo, 0), 4) as debiti_su_attivo,
    round(patrimonio_netto / nullif(attivo, 0), 4) as patrimonio_su_attivo
from totali
