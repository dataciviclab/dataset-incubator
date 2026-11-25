-- SAI Progetti: aggregazione per regione × anno × tipologia
--
-- Nessun filtro su `capienza` (a differenza del mart strutture qui la metrica
-- e' sempre presente, ma teniamo la stessa logica: il conteggio dei progetti
-- non deve dipendere dalla presenza di una metrica).
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
GROUP BY a.anno, a.regione_codice_istat, a.regione_denominazione, a.tipologia
ORDER BY a.anno, a.regione_denominazione
