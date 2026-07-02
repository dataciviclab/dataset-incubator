-- MART: aggregazioni principali per analisi territoriale e settoriale
-- Conserva la granularità originale (singola voce/intervento)

SELECT
    anno,
    sistema_infrastrutturale,
    denominazione,
    soggetto_competente,
    luogo_lavori,
    stato_attuazione,
    anno_ultimazione_previsto,
    costi_mln_euro,
    disponibilita_mln_euro,
    fabbisogno_mln_euro,
    cup,
    link_scheda,
    progressivo,
    livello,
    flag_commissariato_pnrr,
    -- gap finanziario
    CASE
        WHEN costi_mln_euro IS NOT NULL AND disponibilita_mln_euro IS NOT NULL
        THEN costi_mln_euro - disponibilita_mln_euro
        ELSE NULL
    END AS gap_finanziario_mln_euro,
    -- rapporto copertura
    CASE
        WHEN costi_mln_euro IS NOT NULL AND costi_mln_euro > 0
        THEN ROUND(disponibilita_mln_euro / costi_mln_euro * 100, 1)
        ELSE NULL
    END AS pct_copertura,
    -- classificazione macro-stato
    CASE
        WHEN stato_attuazione = 'Lavori conclusi' THEN 'concluso'
        WHEN stato_attuazione IN ('Lavori in corso', 'Opere con esecutore individuato', 'Gara aggiudicata',
                                   'Gara non aggiudicata', 'Opere con bando di gara per la realizzazione pubblicato')
            THEN 'in corso'
        WHEN stato_attuazione IN ('Progettazione preliminare', 'Progettazione definitiva', 'Progettazione esecutiva',
                                   'Studio di fattibilità')
            THEN 'progettazione'
        WHEN stato_attuazione IN ('Contratto rescisso', 'Lavori sospesi', 'Procedimento interrotto')
            THEN 'bloccato'
        ELSE 'non indicato'
    END AS macro_stato
FROM clean_input
