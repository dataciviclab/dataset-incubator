SELECT
    missione,
    descrizione_missione,
    componente,
    descrizione_componente,
    COUNT(DISTINCT cup) AS n_progetti,
    ROUND(SUM(fin_pnrr)) AS tot_fin_pnrr,
    ROUND(SUM(fin_totale)) AS tot_fin_totale,
    ROUND(AVG(fin_totale)) AS media_fin_totale,
    COUNT(DISTINCT soggetto_attuatore) AS n_soggetti_attuatori,
    COUNT(DISTINCT cup_codice_settore) AS n_settori
FROM clean_input
GROUP BY missione, descrizione_missione, componente, descrizione_componente
