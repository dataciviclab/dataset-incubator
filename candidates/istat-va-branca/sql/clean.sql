-- VA per industria — Conti territoriali ISTAT (93_1227)
-- Canale: dbnomics CSV lungo · macros toolkit

SELECT
    normalize_string(REF_AREA)                       AS territorio_codice,
    CASE normalize_string(REF_AREA)
        WHEN 'ITC1' THEN 'Piemonte'
        WHEN 'ITC2' THEN 'Valle d''Aosta'
        WHEN 'ITC3' THEN 'Liguria'
        WHEN 'ITC4' THEN 'Lombardia'
        WHEN 'ITD1' THEN 'Provincia Autonoma Bolzano'
        WHEN 'ITD2' THEN 'Provincia Autonoma Trento'
        WHEN 'ITD3' THEN 'Veneto'
        WHEN 'ITD4' THEN 'Friuli-Venezia Giulia'
        WHEN 'ITD5' THEN 'Emilia-Romagna'
        WHEN 'ITE1' THEN 'Toscana'
        WHEN 'ITE2' THEN 'Umbria'
        WHEN 'ITE3' THEN 'Marche'
        WHEN 'ITE4' THEN 'Lazio'
        WHEN 'ITF1' THEN 'Abruzzo'
        WHEN 'ITF2' THEN 'Molise'
        WHEN 'ITF3' THEN 'Campania'
        WHEN 'ITF4' THEN 'Puglia'
        WHEN 'ITF5' THEN 'Basilicata'
        WHEN 'ITF6' THEN 'Calabria'
        WHEN 'ITG1' THEN 'Sicilia'
        WHEN 'ITG2' THEN 'Sardegna'
        ELSE normalize_string(REF_AREA)
    END                                             AS territorio_nome,
    'regione'                                       AS livello,
    cast_int(TIME_PERIOD)                           AS anno,
    normalize_string(BRKDW_INDUSTRY_NACE_REV2)      AS nace_codice,
    normalize_string(DATA_TYPE_AGGR)                AS tipo_dato_codice,
    CASE normalize_string(DATA_TYPE_AGGR)
        WHEN 'B1G_B_W2_S1' THEN 'VA'
        WHEN 'B1GQ_B_W2_S1' THEN 'PIL'
        ELSE normalize_string(DATA_TYPE_AGGR)
    END                                             AS tipo_dato,
    normalize_string(VALUATION)                     AS valutazione_codice,
    cast_double(OBS_VALUE)                          AS valore_mln_eu
FROM raw_input
WHERE
    normalize_string(REF_AREA) LIKE 'IT%'
    AND length(normalize_string(REF_AREA)) = 4
    AND cast_int(TIME_PERIOD) BETWEEN 1995 AND 2023
    AND normalize_string(BRKDW_INDUSTRY_NACE_REV2) IS NOT NULL
    AND normalize_string(BRKDW_INDUSTRY_NACE_REV2) <> 'Z'
    AND normalize_string(DATA_TYPE_AGGR) = 'B1G_B_W2_S1'
    AND normalize_string(VALUATION) IN ('V', 'L_2020')
    AND cast_double(OBS_VALUE) IS NOT NULL
