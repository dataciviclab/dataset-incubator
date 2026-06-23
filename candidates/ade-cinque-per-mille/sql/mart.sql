-- Mart 5x1000: enti beneficiari per regione, categoria e anno
-- Aggrega a livello regionale per analisi territoriale

SELECT
    anno,
    regione,
    COUNT(DISTINCT codice_fiscale) AS num_enti,
    COUNT(DISTINCT CASE WHEN flag_ets_onlus THEN codice_fiscale END) AS enti_ets_onlus,
    COUNT(DISTINCT CASE WHEN flag_asd THEN codice_fiscale END) AS enti_asd,
    COUNT(DISTINCT CASE WHEN flag_ricerca_scientifica THEN codice_fiscale END) AS enti_ricerca_scientifica,
    COUNT(DISTINCT CASE WHEN flag_ricerca_sanitaria THEN codice_fiscale END) AS enti_ricerca_sanitaria,
    COUNT(DISTINCT CASE WHEN flag_comune THEN codice_fiscale END) AS enti_comune,
    COUNT(DISTINCT CASE WHEN flag_beni_culturali THEN codice_fiscale END) AS enti_beni_culturali,
    COUNT(DISTINCT CASE WHEN flag_area_protetta THEN codice_fiscale END) AS enti_area_protetta,
    SUM(numero_scelte) AS totale_scelte,
    ROUND(SUM(importo_totale_erogabile)::NUMERIC, 2) AS importo_totale_erogabile,
    ROUND(AVG(importo_totale_erogabile)::NUMERIC, 2) AS importo_medio_per_ente
FROM clean_input
GROUP BY anno, regione
ORDER BY anno, importo_totale_erogabile DESC
