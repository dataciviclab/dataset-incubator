-- mart_saldi_regionali — Saldo migratorio per regione × anno
--
-- 1 riga = 1 regione × anno: arrivi, partenze, saldo netto,
-- flussi interni (dentro la stessa regione) e quota flussi interni.
-- Include ESTERO come entità (flussi da/verso l'estero).
-- Serve per: regioni che perdono/attraggono (D1), Lombardia hub (D6),
-- regioni spugna (D10), Sardegna saldo ~0 (D11), autosufficienza (D4).
--
-- PK: (regione, anno)

WITH arrivi AS (
    SELECT anno, arrivo AS regione, SUM(totale) AS arrivi
    FROM clean_input
    WHERE totale IS NOT NULL AND arrivo IS NOT NULL
    GROUP BY anno, arrivo
),
partenze AS (
    SELECT anno, partenza AS regione, SUM(totale) AS partenze
    FROM clean_input
    WHERE totale IS NOT NULL AND partenza IS NOT NULL
    GROUP BY anno, partenza
),
interni AS (
    SELECT anno, partenza AS regione, SUM(totale) AS flussi_interni
    FROM clean_input
    WHERE totale IS NOT NULL AND partenza IS NOT NULL AND partenza = arrivo
    GROUP BY anno, partenza
),
tutte AS (
    SELECT anno, regione FROM arrivi
    UNION
    SELECT anno, regione FROM partenze
    UNION
    SELECT anno, regione FROM interni
)
SELECT
    t.anno,
    t.regione,
    COALESCE(a.arrivi, 0) AS arrivi,
    COALESCE(p.partenze, 0) AS partenze,
    COALESCE(a.arrivi, 0) - COALESCE(p.partenze, 0) AS saldo_netto,
    COALESCE(i.flussi_interni, 0) AS flussi_interni,
    ROUND(
        100.0 * COALESCE(i.flussi_interni, 0)
        / NULLIF(COALESCE(a.arrivi, 0) + COALESCE(p.partenze, 0) - COALESCE(i.flussi_interni, 0), 0),
        1
    ) AS quota_interni_pct
FROM tutte t
LEFT JOIN arrivi a USING (anno, regione)
LEFT JOIN partenze p USING (anno, regione)
LEFT JOIN interni i USING (anno, regione)
ORDER BY t.anno, saldo_netto DESC
