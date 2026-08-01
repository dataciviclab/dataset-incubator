-- mart_profilo_carica — Profilo degli amministratori per carica
--
-- 1 riga = 1 carica (Sindaco, Assessore, Consigliere, ...): conteggi,
-- età media (al 2026-06-01), % femmine, n comuni.
-- Serve per: composizione della classe politica locale (README domanda
-- principale), quanti per carica, differenze demografiche per carica.
--
-- PK: (descrizione_carica)

SELECT
    descrizione_carica,
    COUNT(*) AS n_amministratori,
    COUNT(DISTINCT codice_dait_completo) AS n_comuni,
    ROUND(AVG(DATE_DIFF('year', data_nascita, DATE '2026-06-01')), 1) AS eta_media,
    ROUND(100.0 * SUM(CASE WHEN sesso = 'F' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) AS quota_femmine_pct,
    ROUND(100.0 * SUM(CASE WHEN sesso = 'M' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) AS quota_maschi_pct
FROM clean_input
WHERE descrizione_carica IS NOT NULL
GROUP BY descrizione_carica
ORDER BY n_amministratori DESC
