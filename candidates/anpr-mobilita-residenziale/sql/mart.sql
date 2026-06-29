-- mart.sql — anpr_mobilita_residenziale
-- Dati pass-through con arrotondamenti

SELECT
    anno, mese,
    partenza, cod_regione_partenza,
    arrivo, cod_regione_arrivo,
    totale
FROM clean_input
