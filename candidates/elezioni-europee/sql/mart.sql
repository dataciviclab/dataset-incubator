SELECT
    data_elezione,
    circoscrizione,
    regione,
    provincia,
    comune,
    lista,
    SUM(COALESCE(voti_lista, 0)) AS voti_lista,
    SUM(COALESCE(elettori, 0)) AS elettori,
    SUM(COALESCE(votanti, 0)) AS votanti
FROM clean_input
GROUP BY data_elezione, circoscrizione, regione, provincia, comune, lista
