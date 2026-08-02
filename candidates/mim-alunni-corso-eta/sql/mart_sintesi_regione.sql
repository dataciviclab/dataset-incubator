-- mart_sintesi_regione — Alunni per regione × ordine
--
-- 1 riga = 1 regione × ordine (ultimo anno disponibile): alunni, quota %
-- sul nazionale, n comuni. Serve per: distribuzione territoriale degli
-- alunni, benchmark regionale.
--
-- PK: (regione, ordine_scuola)

SELECT
    regione,
    ordine_scuola,
    SUM(alunni) AS alunni,
    ROUND(
        100.0 * SUM(alunni) / NULLIF(SUM(SUM(alunni)) OVER (PARTITION BY ordine_scuola), 0),
        1
    ) AS quota_nazionale_pct,
    COUNT(DISTINCT codice_scuola) AS n_scuole
FROM clean_input
WHERE regione IS NOT NULL AND alunni IS NOT NULL
GROUP BY regione, ordine_scuola
ORDER BY ordine_scuola, alunni DESC
