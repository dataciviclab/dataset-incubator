-- Patrimonio delle aziende sanitarie per regione e anno.
--
-- I totali generali (AZZ999 "D) TOTALE ATTIVO", PZZ999 "F) TOTALE PASSIVO E
-- PATRIMONIO NETTO") NON sono affidabili: mancano in 9 regioni nel 2024 e in
-- tutte nel 2012. I totali di sezione (*Z999) invece ci sono quasi sempre,
-- quindi attivo e passivo si derivano dalla somma delle sezioni. Il totale
-- pubblicato resta come colonna di controllo, non come misura.
with voci as (
    select
        anno,
        codice_regione,
        any_value(descrizione_regione) as descrizione_regione,
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
    group by anno, codice_regione
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
    -- controllo: attivo derivato vs passivo derivato (deve essere ~0)
    round(attivo - passivo, 2) as quadratura,
    -- controllo: totale pubblicato dalla fonte, quando presente
    attivo_pubblicato,
    passivo_pubblicato,
    round(debiti / nullif(attivo, 0), 4) as debiti_su_attivo,
    round(patrimonio_netto / nullif(attivo, 0), 4) as patrimonio_su_attivo
from totali
