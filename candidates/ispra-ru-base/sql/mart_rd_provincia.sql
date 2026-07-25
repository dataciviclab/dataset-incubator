-- ISPRA: RD% medio per provincia e anno
-- Media pesata (su popolazione) della RD%, con minimo, massimo e deviazione
-- tra i comuni della provincia. Per confrontare performance territoriali.
SELECT
    anno,
    regione,
    provincia,
    COUNT(*) AS comuni,
    ROUND(SUM(popolazione), 0) AS popolazione_totale,
    -- RD% medio pesato per popolazione
    ROUND(SUM(percentuale_rd * popolazione) / NULLIF(SUM(popolazione), 0), 2) AS rd_media_ponderata,
    -- RD% semplice (media aritmetica tra comuni)
    ROUND(AVG(percentuale_rd), 2) AS rd_media_semplice,
    ROUND(MIN(percentuale_rd), 2) AS rd_minimo,
    ROUND(MAX(percentuale_rd), 2) AS rd_massimo,
    ROUND(STDDEV_SAMP(percentuale_rd), 2) AS rd_devstd,
    -- kg pro-capite medi (pesati)
    ROUND(SUM(totale_ru_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0), 1) AS kg_ru_procapite
FROM clean_input
WHERE popolazione > 0
  AND provincia IS NOT NULL
GROUP BY anno, regione, provincia
ORDER BY anno DESC, rd_media_ponderata DESC
