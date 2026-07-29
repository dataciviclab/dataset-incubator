-- Mart: voti per quesito referendario × comune
-- Esteso con affluenza, % SI/NO, esito

SELECT
    data_elezione,
    EXTRACT(YEAR FROM data_elezione) AS anno,
    regione,
    provincia,
    comune,
    num_quesito,
    -- Elettori e votanti (uso ANY_VALUE perché costanti per comune×quesito)
    ANY_VALUE(elettori) AS elettori,
    ANY_VALUE(votanti) AS votanti,
    -- Voti
    SUM(voti_si) AS voti_si,
    SUM(voti_no) AS voti_no,
    SUM(schede_nulle) AS schede_nulle,
    SUM(schede_bianche) AS schede_bianche,
    SUM(schede_contestate) AS schede_contestate,
    -- Metriche calcolate
    ROUND(CAST(ANY_VALUE(votanti) AS DOUBLE) / NULLIF(CAST(ANY_VALUE(elettori) AS DOUBLE), 0) * 100, 2) AS affluenza_pct,
    ROUND(CAST(SUM(voti_si) AS DOUBLE) / NULLIF(SUM(voti_si) + SUM(voti_no), 0) * 100, 2) AS pct_si,
    ROUND(CAST(SUM(voti_no) AS DOUBLE) / NULLIF(SUM(voti_si) + SUM(voti_no), 0) * 100, 2) AS pct_no,
    -- Esito: vince SI se > 50% dei voti validi E quorum raggiunto (votanti > 50% elettori)
    CASE
        WHEN SUM(voti_si) > SUM(voti_no) AND CAST(ANY_VALUE(votanti) AS DOUBLE) > CAST(ANY_VALUE(elettori) AS DOUBLE) * 0.5 THEN 'SI'
        WHEN SUM(voti_si) > SUM(voti_no) THEN 'SI (no quorum)'
        WHEN SUM(voti_no) > SUM(voti_si) AND CAST(ANY_VALUE(votanti) AS DOUBLE) > CAST(ANY_VALUE(elettori) AS DOUBLE) * 0.5 THEN 'NO'
        ELSE 'NO (no quorum)'
    END AS esito
FROM clean_input
GROUP BY data_elezione, regione, provincia, comune, num_quesito
ORDER BY data_elezione DESC, regione, provincia, comune, num_quesito
