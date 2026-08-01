-- mart_profilo_demografico — Profilo demografico per carica
--
-- 1 riga = 1 carica: distribuzione per sesso e classe di età, età media.
-- Serve per: quante donne elette (README), età media di sindaci/assessori/
-- consiglieri, composizione anagrafica della classe politica locale.
--
-- PK: (descrizione_carica, sesso)

SELECT
    descrizione_carica,
    sesso,
    COUNT(*) AS n_amministratori,
    ROUND(AVG(DATE_DIFF('year', data_nascita, DATE '2026-06-01')), 1) AS eta_media,
    SUM(CASE WHEN DATE_DIFF('year', data_nascita, DATE '2026-06-01') < 30 THEN 1 ELSE 0 END) AS n_under_30,
    SUM(CASE WHEN DATE_DIFF('year', data_nascita, DATE '2026-06-01') BETWEEN 30 AND 49 THEN 1 ELSE 0 END) AS n_30_49,
    SUM(CASE WHEN DATE_DIFF('year', data_nascita, DATE '2026-06-01') BETWEEN 50 AND 64 THEN 1 ELSE 0 END) AS n_50_64,
    SUM(CASE WHEN DATE_DIFF('year', data_nascita, DATE '2026-06-01') >= 65 THEN 1 ELSE 0 END) AS n_over_65
FROM clean_input
WHERE descrizione_carica IS NOT NULL AND sesso IS NOT NULL AND data_nascita IS NOT NULL
GROUP BY descrizione_carica, sesso
ORDER BY descrizione_carica, sesso
