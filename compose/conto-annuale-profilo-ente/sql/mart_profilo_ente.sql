-- Profilo Ente — per ente singolo
-- Esclude enti con meno di 5 dipendenti (metriche procapite distorti)
-- e enti con costo_totale negativo (rimborsi UE eccedono le voci positive)
SELECT
    anno,
    istituzione,
    desc_istituzione,
    codi_comparto,
    desc_comparto,
    codi_tipo_istituzione,
    ROUND(dipendenti, 0) AS dipendenti,
    ROUND(donne * 100.0 / NULLIF(dipendenti, 0), 1) AS pct_donne,
    eta_media,
    anzianita_media,
    pct_laureati,
    retribuzione_totale,
    costo_totale,
    CASE WHEN dipendenti > 0 AND retribuzione_totale IS NOT NULL
        THEN ROUND(retribuzione_totale / dipendenti, 0)
        ELSE NULL END AS retribuzione_procapite,
    CASE WHEN dipendenti > 0 AND costo_totale IS NOT NULL AND costo_totale > 0
        THEN ROUND(costo_totale / dipendenti, 0)
        ELSE NULL END AS costo_procapite,
    assenze_totali,
    CASE WHEN dipendenti > 0 AND assenze_totali IS NOT NULL
        THEN ROUND(assenze_totali / dipendenti, 1)
        ELSE NULL END AS assenze_procapite
FROM clean_input
WHERE dipendenti >= 5
ORDER BY desc_comparto, desc_istituzione
