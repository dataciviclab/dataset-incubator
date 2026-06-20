SELECT
    data_elezione,
    cod_tipo_elezione,
    circoscrizione,
    comune,
    descr_lista,
    SUM(voti_lista) AS tot_voti_lista,
    COUNT(DISTINCT collegio_uninominale) AS n_collegi,
    COUNT(DISTINCT cognome_candidato || ' ' || nome_candidato) AS n_candidati
FROM clean_input
GROUP BY data_elezione, cod_tipo_elezione, circoscrizione, comune, descr_lista
