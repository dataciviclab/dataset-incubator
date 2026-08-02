-- mart_comune — Alunni per comune (ultimo anno) con benchmark provinciale
--
-- 1 riga = 1 comune × ordine: alunni, quota sul totale provinciale.
-- Serve per: dettaglio comunale con contesto (pattern comuni/sintesi/trend).
--
-- PK: (codice_comune_scuola, ordine_scuola)

WITH per_comune AS (
    SELECT
        codice_comune_scuola,
        comune,
        regione,
        provincia,
        ordine_scuola,
        SUM(alunni) AS alunni
    FROM clean_input
    WHERE codice_comune_scuola IS NOT NULL AND alunni IS NOT NULL
    GROUP BY codice_comune_scuola, comune, regione, provincia, ordine_scuola
),
per_provincia AS (
    SELECT provincia, ordine_scuola, SUM(alunni) AS alunni_provincia
    FROM per_comune
    GROUP BY provincia, ordine_scuola
)
SELECT
    c.codice_comune_scuola,
    c.comune,
    c.regione,
    c.provincia,
    c.ordine_scuola,
    c.alunni,
    ROUND(100.0 * c.alunni / NULLIF(p.alunni_provincia, 0), 2) AS quota_provinciale_pct
FROM per_comune c
JOIN per_provincia p USING (provincia, ordine_scuola)
ORDER BY c.ordine_scuola, c.alunni DESC
