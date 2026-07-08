SELECT
    data_elezione,
    regione,
    provincia,
    comune,
    turno,
    candidato,
    lista,
    SUM(COALESCE(voti_candidato, 0)) AS voti_candidato,
    SUM(COALESCE(voti_lista, 0)) AS voti_lista,
    MAX(COALESCE(seggi_lista, 0)) AS seggi_lista,
    MAX(COALESCE(elettori, 0)) AS elettori,
    MAX(COALESCE(votanti, 0)) AS votanti
FROM clean_input
GROUP BY data_elezione, regione, provincia, comune, turno, candidato, lista
