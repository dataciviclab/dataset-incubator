-- mart.sql - malasanita_c_strutture_ricovero - mart_regioni
-- Output: una riga per regione / PA con dotazione ospedaliera aggregata

SELECT
    anno,
    codice_regione,
    regione,
    SUM(totale_personale) AS personale_ospedaliero,
    SUM(medici) AS medici_ospedalieri,
    SUM(infermieri) AS infermieri,
    SUM(posti_letto_previsti) AS posti_letto_previsti,
    SUM(posti_letto_utilizzati) AS posti_letto_utilizzati
FROM clean_input
GROUP BY anno, codice_regione, regione
ORDER BY codice_regione
