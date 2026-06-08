-- Mart: Posti letto per regione, disciplina e anno
SELECT
    ci.anno,
    ci.descrizione_regione,
    ci.codice_regione,
    ci.descrizione_disciplina,
    ci.codice_disciplina,
    ci.tipo_di_disciplina,
    COUNT(DISTINCT ci.codice_struttura) AS strutture_con_reparto,
    SUM(ci.posti_letto_degenza_ordinaria) AS tot_posti_letto_degenza_ordinaria,
    SUM(ci.posti_letto_day_hospital) AS tot_posti_letto_day_hospital,
    SUM(ci.posti_letto_day_surgery) AS tot_posti_letto_day_surgery,
    SUM(ci.totale_posti_letto) AS tot_posti_letto,
    SUM(ci.n_reparti) AS tot_reparti
FROM clean_input ci
GROUP BY ci.anno, ci.descrizione_regione, ci.codice_regione,
         ci.descrizione_disciplina, ci.codice_disciplina, ci.tipo_di_disciplina
ORDER BY ci.anno, ci.descrizione_regione, ci.descrizione_disciplina
