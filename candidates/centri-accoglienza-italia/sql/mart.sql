-- Centri accoglienza: aggregazione per regione × anno × tipologia
-- Colonne clean_input: rilevazione_data, centro_id, ..., regione_denominazione, regione_codice_istat,
--   ente_gestore, costo_giornaliero_per_ospite, presenze_giornaliere, capienza, tipologia_centro, ...

SELECT
    a.anno,
    a.regione_codice_istat,
    a.regione_denominazione,
    a.tipologia_centro,
    COUNT(DISTINCT a.centro_id) AS numero_centri,
    SUM(a.capienza) AS capienza_totale,
    SUM(a.presenze_giornaliere) AS presenze_totali,
    AVG(a.costo_giornaliero_per_ospite) AS costo_medio_giornaliero,
    AVG(a.presenze_giornaliere / NULLIF(a.capienza, 0)) * 100 AS tasso_occupazione_pct
FROM clean_input a
WHERE a.operativita = 'ATTIVO'
GROUP BY a.anno, a.regione_codice_istat, a.regione_denominazione, a.tipologia_centro
ORDER BY a.anno, a.regione_denominazione, a.tipologia_centro
