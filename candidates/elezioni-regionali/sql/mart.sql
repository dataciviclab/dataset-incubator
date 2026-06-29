SELECT
    data_elezione,
    regione,
    circoscrizione,
    provincia,
    comune,
    lista,
    candidato,
    SUM(voti_lista) AS tot_voti_lista,
    MAX(voti_candidato) AS voti_candidato,  -- stesso valore su tutte le righe del presidente
    MAX(elettori) AS elettori,
    MAX(votanti) AS votanti,
    MAX(schede_bianche) AS schede_bianche
FROM clean_input
GROUP BY data_elezione, regione, circoscrizione, provincia, comune, lista, candidato
