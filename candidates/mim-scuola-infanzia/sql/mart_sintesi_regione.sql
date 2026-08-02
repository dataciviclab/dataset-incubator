-- mart_sintesi_regione — Bambini infanzia per regione (ultimo anno)
--
-- 1 riga = 1 regione: bambini italiani/non italiani, quota stranieri,
-- n scuole, quota sul totale nazionale. Serve per: distribuzione
-- territoriale, divari regionali nella presenza di bambini stranieri.
--
-- PK: (regione)

WITH per_regione AS (
    SELECT
        regione,
        SUM(bambini_italiani) AS bambini_italiani,
        SUM(bambini_non_italiani) AS bambini_non_italiani,
        SUM(bambini_totale) AS bambini_totale,
        COUNT(DISTINCT codice_scuola) AS n_scuole
    FROM clean_input
    WHERE regione IS NOT NULL AND bambini_totale IS NOT NULL
    GROUP BY regione
),
totale_nazionale AS (
    SELECT SUM(bambini_totale) AS tot FROM per_regione
)
SELECT
    r.regione,
    r.bambini_italiani,
    r.bambini_non_italiani,
    r.bambini_totale,
    ROUND(100.0 * r.bambini_non_italiani / NULLIF(r.bambini_totale, 0), 2) AS quota_non_italiani_pct,
    r.n_scuole,
    ROUND(100.0 * r.bambini_totale / NULLIF(t.tot, 0), 1) AS quota_nazionale_pct
FROM per_regione r
CROSS JOIN totale_nazionale t
ORDER BY r.bambini_totale DESC
