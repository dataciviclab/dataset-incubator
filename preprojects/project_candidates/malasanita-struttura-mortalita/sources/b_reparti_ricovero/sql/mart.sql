-- mart.sql - malasanita_b_reparti_ricovero - mart_regioni
-- Output: una riga per regione / PA con dotazione per reparto e ampiezza disciplinare
-- Nota metodologica:
-- - i posti letto aggregati qui sono quasi sovrapposti a C a livello regionale
-- - il valore aggiunto di B e soprattutto il dettaglio per disciplina/reparto

SELECT
    anno,
    codice_regione,
    regione,
    COUNT(*) AS n_reparti,
    COUNT(DISTINCT codice_struttura) AS n_strutture_con_reparti,
    COUNT(DISTINCT codice_disciplina) AS n_discipline_attive,
    SUM(posti_letto_degenza_ordinaria) AS posti_letto_degenza_ordinaria,
    SUM(posti_letto_day_hospital) AS posti_letto_day_hospital,
    SUM(posti_letto_day_surgery) AS posti_letto_day_surgery,
    SUM(posti_letto_day_hospital + posti_letto_day_surgery) AS posti_letto_diurni,
    SUM(posti_letto_utilizzati) AS posti_letto_utilizzati
FROM clean_input
GROUP BY anno, codice_regione, regione
ORDER BY codice_regione
