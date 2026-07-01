SELECT
    id_notice_cn,
    ted_notice_url,
    anno_pubblicazione,
    data_invio,
    stazione_appaltante_nome,
    stazione_appaltante_citta,
    stazione_appaltante_cap,
    paese,
    tipo_stazione_appaltante,
    attivita_principale,
    tipo_contratto,
    nuts_luogo_esecuzione,
    cpv_codice,
    cpv_codici_aggiuntivi,
    id_lotto,
    n_lotti,
    valore_euro,
    valore_euro_fin_1,
    flag_fondi_ue,
    flag_accordo_quadro,
    flag_opzioni,
    flag_rinnovo,
    durata_mesi,
    tipo_procedura,
    flag_accelerata,
    codice_criterio_aggiudicazione,
    peso_prezzo,
    criteri_qualitativi,
    flag_asta_elettronica,
    data_scadenza_offerte,
    flag_appalto_ricorrente,
    flag_cancellato,
    n_correzioni,
    -- Flag per bandi sopra soglia (valore > 140K per servizi/forniture, > 5.382M per lavori)
    CASE
        WHEN tipo_contratto = 'W' AND valore_euro >= 5382000 THEN TRUE
        WHEN tipo_contratto IN ('S', 'G') AND valore_euro >= 140000 THEN TRUE
        WHEN tipo_contratto = 'C' AND valore_euro >= 5382000 THEN TRUE
        ELSE FALSE
    END AS flag_soprasoglia_ue,
    -- Range di valore
    CASE
        WHEN valore_euro IS NULL THEN 'ND'
        WHEN valore_euro < 40000 THEN 'micro (< 40K)'
        WHEN valore_euro < 140000 THEN 'piccolo (40K-140K)'
        WHEN valore_euro < 1000000 THEN 'medio (140K-1M)'
        WHEN valore_euro < 5000000 THEN 'grande (1M-5M)'
        WHEN valore_euro < 50000000 THEN 'molto grande (5M-50M)'
        ELSE 'strategico (> 50M)'
    END AS fascia_valore,
    -- NUTS regione
    CASE
        WHEN LEFT(nuts_luogo_esecuzione, 4) = 'ITC' THEN 'Piemonte/ValleAosta/Lombardia'
        WHEN LEFT(nuts_luogo_esecuzione, 4) = 'ITF' THEN 'Sud'
        WHEN LEFT(nuts_luogo_esecuzione, 4) = 'ITH' THEN 'Nord-Est'
        WHEN LEFT(nuts_luogo_esecuzione, 4) = 'ITI' THEN 'Centro'
        WHEN LEFT(nuts_luogo_esecuzione, 4) = 'ITG' THEN 'Isole'
        ELSE 'ND'
    END AS macroarea_nuts1
FROM clean_input
