-- SAI Strutture: aggregazione per regione × anno × tipologia struttura
SELECT
    a.anno,
    a.regione_codice_istat,
    a.regione_denominazione,
    a.sai_struttura_tipologia,
    a.sai_progetto_tipologia,
    COUNT(DISTINCT a.sai_struttura_id) AS strutture,
    SUM(a.capienza) AS capienza_totale,
    SUM(a.presenze_giornaliere) AS presenze_totali
FROM clean_input a
WHERE a.capienza > 0
GROUP BY a.anno, a.regione_codice_istat, a.regione_denominazione,
         a.sai_struttura_tipologia, a.sai_progetto_tipologia
ORDER BY a.anno, a.regione_denominazione
