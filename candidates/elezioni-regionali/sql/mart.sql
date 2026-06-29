SELECT
    data_elezione,
    regione,
    circoscrizione,
    provincia,
    comune,
    lista,
    SUM(voti_lista) AS tot_voti_lista,
    SUM(voti_candidato) AS tot_voti_candidato,
    COUNT(DISTINCT candidato) AS n_candidati,
    MAX(elettori) AS elettori,
    MAX(votanti) AS votanti,
    MAX(schede_bianche) AS schede_bianche
FROM clean_input
GROUP BY data_elezione, regione, circoscrizione, provincia, comune, lista
