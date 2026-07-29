-- Mart: voti per lista alle elezioni politiche (Camera/Senato)
-- Ogni riga: comune × lista × Camera_Senato × anno

SELECT
    data_elezione,
    EXTRACT(YEAR FROM data_elezione) AS anno,
    camera_senato,
    circoscrizione,
    provincia,
    comune,
    lista,
    descr_lista,
    SUM(voti_lista) AS tot_voti_lista,
    -- Elettori/votanti (costanti per comune×camera)
    MAX(elettori_totali) AS elettori_totali,
    MAX(votanti_totali) AS votanti_totali,
    MAX(schede_biache) AS schede_biache,
    -- Affluenza calcolata
    ROUND(CAST(MAX(votanti_totali) AS DOUBLE) / NULLIF(CAST(MAX(elettori_totali) AS DOUBLE), 0) * 100, 2) AS affluenza_pct,
    -- % lista sul totale voti della circoscrizione (ponderata)
    SUM(voti_lista) * 1.0 / NULLIF(SUM(SUM(voti_lista)) OVER (PARTITION BY data_elezione, camera_senato, circoscrizione, comune), 0) * 100 AS pct_lista_comune
FROM clean_input
WHERE voti_lista IS NOT NULL AND voti_lista >= 0
GROUP BY data_elezione, camera_senato, circoscrizione, provincia, comune, lista, descr_lista
ORDER BY data_elezione, camera_senato, circoscrizione, comune, tot_voti_lista DESC
