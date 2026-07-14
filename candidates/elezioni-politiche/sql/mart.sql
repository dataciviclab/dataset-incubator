SELECT
    data_elezione,
    camera_senato,
    circoscrizione,
    comune,
    lista,
    SUM(voti_lista) AS tot_voti_lista,
    MAX(elettori_totali) AS elettori_totali,
    MAX(votanti_totali) AS votanti_totali,
    MAX(schede_biache) AS schede_biache
FROM clean_input
WHERE voti_lista IS NOT NULL AND voti_lista >= 0
GROUP BY data_elezione, camera_senato, circoscrizione, comune, lista
ORDER BY data_elezione, camera_senato, circoscrizione, comune, tot_voti_lista DESC
