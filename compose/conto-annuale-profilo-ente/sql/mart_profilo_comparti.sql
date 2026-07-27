-- Profilo Ente — aggregato per comparto e tipo istituzione
SELECT
    anno,
    codi_comparto,
    desc_comparto,
    codi_tipo_istituzione,
    COUNT(DISTINCT istituzione) AS enti,
    ROUND(SUM(dipendenti), 0) AS tot_dipendenti,
    ROUND(SUM(donne) * 100.0 / NULLIF(SUM(dipendenti), 0), 1) AS pct_donne,
    ROUND(AVG(eta_media), 1) AS eta_media,
    ROUND(AVG(anzianita_media), 1) AS anzianita_media,
    ROUND(AVG(pct_laureati), 1) AS pct_laureati,
    ROUND(SUM(retribuzione_totale) / NULLIF(SUM(dipendenti), 0), 0) AS retribuzione_media_procapite,
    ROUND(SUM(costo_totale) / NULLIF(SUM(dipendenti), 0), 0) AS costo_medio_procapite,
    ROUND(SUM(assenze_totali) / NULLIF(SUM(dipendenti), 0), 1) AS assenze_giorni_procapite
FROM clean_input
WHERE dipendenti > 0
GROUP BY 1, 2, 3, 4
ORDER BY anno DESC, tot_dipendenti DESC
