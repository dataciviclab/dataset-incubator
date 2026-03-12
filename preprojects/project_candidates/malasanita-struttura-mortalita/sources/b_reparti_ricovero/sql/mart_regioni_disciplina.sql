-- mart_regioni_disciplina.sql - malasanita_b_reparti_ricovero
-- Output: una riga per regione / PA x disciplina
-- Serve per analisi di offerta disciplinare; non entra nel compose regionale corrente.

SELECT
    anno,
    codice_regione,
    regione,
    codice_disciplina,
    disciplina,
    COUNT(*) AS n_reparti,
    COUNT(DISTINCT codice_struttura) AS n_strutture_con_disciplina,
    SUM(posti_letto_degenza_ordinaria) AS posti_letto_degenza_ordinaria,
    SUM(posti_letto_day_hospital) AS posti_letto_day_hospital,
    SUM(posti_letto_day_surgery) AS posti_letto_day_surgery,
    SUM(posti_letto_day_hospital + posti_letto_day_surgery) AS posti_letto_diurni,
    SUM(posti_letto_utilizzati) AS posti_letto_utilizzati
FROM clean_input
GROUP BY anno, codice_regione, regione, codice_disciplina, disciplina
ORDER BY codice_regione, codice_disciplina
