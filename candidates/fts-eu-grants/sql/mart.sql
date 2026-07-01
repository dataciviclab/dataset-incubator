SELECT
    anno,
    beneficiario_nome,
    beneficiario_partita_iva,
    flag_no_profit,
    flag_ong,
    beneficiario_citta,
    nuts2,
    importo_contrattato,
    importo_contrattato_stimato,
    importo_consumato_stimato,
    oggetto_contributo,
    dipartimento_responsabile,
    nome_programma,
    tipo_finanziamento,
    tipo_beneficiario,
    data_inizio_progetto,
    data_fine_progetto,
    tipo_contratto,
    tipo_gestione,
    -- Classificazione per programma
    CASE
        WHEN nome_programma ILIKE '%Horizon%' THEN 'Ricerca (Horizon)'
        WHEN nome_programma ILIKE '%Erasmus%' THEN 'Istruzione (Erasmus+)'
        WHEN nome_programma ILIKE '%Digital Europe%' THEN 'Digitale (DEP)'
        WHEN nome_programma ILIKE '%Creative Europe%' OR nome_programma ILIKE '%Culture%' THEN 'Cultura (Creative Europe)'
        WHEN nome_programma ILIKE '%LIFE%' THEN 'Ambiente (LIFE)'
        WHEN nome_programma ILIKE '%CERV%' OR nome_programma ILIKE '%Citizens%' THEN 'Cittadinanza (CERV)'
        WHEN nome_programma ILIKE '%Health%' OR nome_programma ILIKE '%EU4H%' THEN 'Salute (EU4Health)'
        WHEN nome_programma ILIKE '%Humanitarian%' THEN 'Aiuti umanitari'
        WHEN nome_programma ILIKE '%Migration%' OR nome_programma ILIKE '%AMIF%' THEN 'Migrazione'
        WHEN nome_programma ILIKE '%Research Fund%' OR nome_programma ILIKE '%RFCS%' THEN 'Ricerca carbone/acciaio'
        ELSE 'Altri programmi'
    END AS categoria_programma,
    -- Classificazione beneficiario
    CASE
        WHEN flag_no_profit = 'Yes' THEN 'Non-profit'
        WHEN flag_ong = 'Yes' THEN 'ONG'
        WHEN tipo_beneficiario ILIKE '%university%' OR tipo_beneficiario ILIKE '%research%' OR tipo_beneficiario ILIKE '%higher%' THEN 'Ricerca/Università'
        WHEN tipo_beneficiario ILIKE '%SME%' OR tipo_beneficiario ILIKE '%enterprise%' OR tipo_beneficiario ILIKE '%company%' THEN 'Impresa'
        WHEN tipo_beneficiario ILIKE '%public%' OR tipo_beneficiario ILIKE '%government%' THEN 'Pubblica Amministrazione'
        ELSE 'Altro'
    END AS tipo_ente,
    -- Range importo
    CASE
        WHEN importo_contrattato IS NULL THEN 'ND'
        WHEN importo_contrattato < 10000 THEN 'micro (<10K)'
        WHEN importo_contrattato < 100000 THEN 'piccolo (10K-100K)'
        WHEN importo_contrattato < 1000000 THEN 'medio (100K-1M)'
        WHEN importo_contrattato < 10000000 THEN 'grande (1M-10M)'
        ELSE 'strategico (>10M)'
    END AS fascia_importo
FROM clean_input
