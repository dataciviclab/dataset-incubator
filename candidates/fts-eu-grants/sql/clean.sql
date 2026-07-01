SELECT
    TRY_CAST(TRY_CAST(anno AS BIGINT) AS INTEGER) AS anno,
    budget::VARCHAR AS budget,
    rif_impegno_giuridico::VARCHAR AS rif_impegno_giuridico,
    rif_bilancio::VARCHAR AS rif_bilancio,
    beneficiario_nome::VARCHAR AS beneficiario_nome,
    beneficiario_partita_iva::VARCHAR AS beneficiario_partita_iva,
    flag_no_profit::VARCHAR AS flag_no_profit,
    flag_ong::VARCHAR AS flag_ong,
    flag_coordinatore::VARCHAR AS flag_coordinatore,
    beneficiario_indirizzo::VARCHAR AS beneficiario_indirizzo,
    beneficiario_citta::VARCHAR AS beneficiario_citta,
    beneficiario_cap::VARCHAR AS beneficiario_cap,
    paese_beneficiario::VARCHAR AS paese_beneficiario,
    nuts2::VARCHAR AS nuts2,
    zona_geografica::VARCHAR AS zona_geografica,
    luogo_azione::VARCHAR AS luogo_azione,
    CASE WHEN importo_contrattato::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(importo_contrattato::VARCHAR, ',', '') AS DOUBLE)
    END AS importo_contrattato,
    CASE WHEN importo_contrattato_stimato::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(importo_contrattato_stimato::VARCHAR, ',', '') AS DOUBLE)
    END AS importo_contrattato_stimato,
    CASE WHEN importo_consumato_stimato::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(importo_consumato_stimato::VARCHAR, ',', '') AS DOUBLE)
    END AS importo_consumato_stimato,
    CASE WHEN impegno_importo_a::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(impegno_importo_a::VARCHAR, ',', '') AS DOUBLE)
    END AS impegno_importo_a,
    CASE WHEN importo_aggiuntivo_ridotto_b::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(importo_aggiuntivo_ridotto_b::VARCHAR, ',', '') AS DOUBLE)
    END AS importo_aggiuntivo_ridotto_b,
    CASE WHEN impegno_totale_a_plus_b::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(impegno_totale_a_plus_b::VARCHAR, ',', '') AS DOUBLE)
    END AS impegno_totale_a_plus_b,
    CASE WHEN impegno_consumato::VARCHAR IN ('-', '', '.') THEN NULL
         ELSE TRY_CAST(REPLACE(impegno_consumato::VARCHAR, ',', '') AS DOUBLE)
    END AS impegno_consumato,
    fonte_dettaglio::VARCHAR AS fonte_dettaglio,
    tipo_spesa::VARCHAR AS tipo_spesa,
    oggetto_contributo::VARCHAR AS oggetto_contributo,
    dipartimento_responsabile::VARCHAR AS dipartimento_responsabile,
    linea_bilancio_codice::VARCHAR AS linea_bilancio_codice,
    linea_bilancio_nome::VARCHAR AS linea_bilancio_nome,
    nome_programma::VARCHAR AS nome_programma,
    tipo_finanziamento::VARCHAR AS tipo_finanziamento,
    codice_gruppo_beneficiario::VARCHAR AS codice_gruppo_beneficiario,
    tipo_beneficiario::VARCHAR AS tipo_beneficiario,
    TRY_CAST(data_inizio_progetto AS DATE) AS data_inizio_progetto,
    TRY_CAST(data_fine_progetto AS DATE) AS data_fine_progetto,
    tipo_contratto::VARCHAR AS tipo_contratto,
    tipo_gestione::VARCHAR AS tipo_gestione,
    paese_beneficiante::VARCHAR AS paese_beneficiante
FROM raw_input
WHERE UPPER(paese_beneficiario::VARCHAR) = 'ITALY'
