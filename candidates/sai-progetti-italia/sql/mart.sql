-- SAI Progetti: aggregazione per regione × anno × tipologia
SELECT
    a.anno,
    a.regione_codice_istat,
    a.regione_denominazione,
    a.tipologia,
    COUNT(DISTINCT a.progetto_codice) AS progetti,
    SUM(a.capienza) AS capienza_totale,
    SUM(a.presenze) AS presenze_totali,
    AVG(a.capienza) AS capienza_media_progetto
FROM clean_input a
WHERE a.capienza > 0
GROUP BY a.anno, a.regione_codice_istat, a.regione_denominazione, a.tipologia
ORDER BY a.anno, a.regione_denominazione
