-- mart_territorio — Composizione amministratori per territorio
--
-- 1 riga = 1 regione × carica: conteggi, % femmine, età media, n comuni.
-- Serve per: differenze Nord/Sud (README), quante donne per regione,
-- distribuzione territoriale della classe politica.
-- NOTA: la regione è il codice DAIT (2 cifre) — non è il codice ISTAT.
--
-- PK: (codice_regione, descrizione_carica)

SELECT
    codice_regione,
    descrizione_carica,
    COUNT(*) AS n_amministratori,
    COUNT(DISTINCT codice_dait_completo) AS n_comuni,
    ROUND(100.0 * SUM(CASE WHEN sesso = 'F' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) AS quota_femmine_pct,
    ROUND(AVG(DATE_DIFF('year', data_nascita, DATE '2026-06-01')), 1) AS eta_media
FROM clean_input
WHERE codice_regione IS NOT NULL AND descrizione_carica IS NOT NULL
GROUP BY codice_regione, descrizione_carica
ORDER BY codice_regione, n_amministratori DESC
