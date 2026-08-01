-- mart_corridoi — Flussi tra coppie origine → destinazione per anno
--
-- 1 riga = 1 corridoio (partenza × arrivo) × anno, con totale trasferimenti.
-- Serve per: esodo Sud→Nord (D2), controesodo Nord→Sud (D3), verso estero
-- (D8), coppie simmetriche "gemelli demografici" (D9), trend dei grandi
-- corridoi (D13).
--
-- PK: (partenza, arrivo, anno)

SELECT
    anno,
    partenza,
    arrivo,
    SUM(totale) AS trasferimenti
FROM clean_input
WHERE totale IS NOT NULL
  AND partenza IS NOT NULL
  AND arrivo IS NOT NULL
GROUP BY anno, partenza, arrivo
ORDER BY anno, trasferimenti DESC
