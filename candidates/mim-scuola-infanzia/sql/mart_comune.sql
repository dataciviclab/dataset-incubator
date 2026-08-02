-- mart_comune — Bambini infanzia per comune (ultimo anno) con benchmark
--
-- 1 riga = 1 comune: bambini italiani/non italiani, quota stranieri,
-- quota sul totale provinciale. Serve per: dettaglio comunale con contesto.
--
-- PK: (codice_comune_scuola)

WITH per_comune AS (
    SELECT
        codice_comune_scuola,
        comune,
        regione,
        provincia,
        SUM(bambini_italiani) AS bambini_italiani,
        SUM(bambini_non_italiani) AS bambini_non_italiani,
        SUM(bambini_totale) AS bambini_totale
    FROM clean_input
    WHERE codice_comune_scuola IS NOT NULL AND bambini_totale IS NOT NULL
    GROUP BY codice_comune_scuola, comune, regione, provincia
),
per_provincia AS (
    SELECT provincia, SUM(bambini_totale) AS bambini_provincia
    FROM per_comune
    GROUP BY provincia
)
SELECT
    c.codice_comune_scuola,
    c.comune,
    c.regione,
    c.provincia,
    c.bambini_italiani,
    c.bambini_non_italiani,
    c.bambini_totale,
    ROUND(100.0 * c.bambini_non_italiani / NULLIF(c.bambini_totale, 0), 2) AS quota_non_italiani_pct,
    ROUND(100.0 * c.bambini_totale / NULLIF(p.bambini_provincia, 0), 2) AS quota_provinciale_pct
FROM per_comune c
JOIN per_provincia p USING (provincia)
ORDER BY c.bambini_totale DESC
