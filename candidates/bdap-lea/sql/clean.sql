-- Modello LEA enti SSN — una riga per ente x voce contabile x anno.
--
-- La fonte contiene tre tipi di riga e due tipi di voce, e vanno distinti prima
-- di qualunque somma:
--   tipo_riga  ente       azienda sanitaria (si somma tra loro)
--              regione    codice 000: ente regione, soggetto reale
--              consolidato codice 999: totale regionale (include gli enti)
--   tipo_voce  totale     19999/29999/39999/48888/49999: le uniche voci
--                         somnabili (49999 = somma delle altre quattro)
--              dettaglio  voci gerarchiche: un genitore contiene i figli,
--                         sommarle tutte moltiplica il totale per ~2,4
with base as (
    select
        cast_int("Anno di Riferimento") as anno_riferimento,
        normalize_string("Codice Regione") as codice_regione,
        normalize_string("Descrizione Regione") as descrizione_regione,
        normalize_string("Codice Ente SSN") as codice_ente_ssn,
        normalize_string("Codice Ente BDAP") as codice_ente_bdap,
        normalize_string("Descrizione Ente") as descrizione_ente,
        normalize_string("Codice Voce Contabile") as codice_voce_contabile,
        normalize_string("Descrizione Voce Contabile") as descrizione_voce_contabile,
        cast_double("Oneri Finanziari") as oneri_finanziari,
        normalize_string("Data Aggiornamento") as data_aggiornamento,
        cast_double("Consumi sanitari") as consumi_sanitari,
        cast_double("Consumi non sanitari") as consumi_non_sanitari,
        cast_double("Prestazioni sanitarie") as prestazioni_sanitarie,
        cast_double("Servizi sanitari") as servizi_sanitari,
        cast_double("Servizi non sanitari") as servizi_non_sanitari,
        cast_double("Personale Sanitario") as personale_sanitario,
        cast_double("Personale Professionale") as personale_professionale,
        cast_double("Personale Tecnico") as personale_tecnico,
        cast_double("Personale Amministrativo") as personale_amministrativo,
        cast_double("Ammortamenti") as ammortamenti,
        cast_double("Sopravvenienze e Insussistenze") as sopravvenienze_e_insussistenze,
        cast_double("Altri costi") as altri_costi,
        cast_double("Importo Totale") as importo_totale
    from raw_input
)

select
    *,
    case
        when codice_voce_contabile in ('19999', '29999', '39999', '48888', '49999')
            then 'totale'
        else 'dettaglio'
    end as tipo_voce,
    case
        when codice_ente_ssn = '000' then 'regione'
        when codice_ente_ssn = '999' then 'consolidato'
        else 'ente'
    end as tipo_riga
from base
where anno_riferimento is not null
