SELECT
    data_elezione,
    regione,
    provincia,
    comune,
    num_quesito,
    SUM(COALESCE(elettori, 0)) AS elettori,
    SUM(COALESCE(votanti, 0)) AS votanti,
    SUM(COALESCE(voti_si, 0)) AS voti_si,
    SUM(COALESCE(voti_no, 0)) AS voti_no,
    SUM(COALESCE(schede_nulle, 0)) AS schede_nulle,
    SUM(COALESCE(schede_bianche, 0)) AS schede_bianche,
    SUM(COALESCE(schede_contestate, 0)) AS schede_contestate
FROM clean_input
GROUP BY data_elezione, regione, provincia, comune, num_quesito
