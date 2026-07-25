-- ISPRA: Ranking comuni per RD% con classe di popolazione
-- Top e bottom comuni per raccolta differenziata, segmentati per
-- fascia demografica (sotto 5k, 5-15k, 15-50k, sopra 50k).
-- Serve per confrontare performance tra comuni simili.
WITH comuni_con_classi AS (
    SELECT
        anno,
        regione,
        provincia,
        comune,
        codice_comune_istat,
        popolazione,
        percentuale_rd,
        totale_ru_tonnellate,
        ROUND(totale_ru_tonnellate * 1000.0 / NULLIF(popolazione, 0), 1) AS kg_ru_procapite,
        CASE
            WHEN popolazione < 5000 THEN 'sotto_5k'
            WHEN popolazione < 15000 THEN '5k_15k'
            WHEN popolazione < 50000 THEN '15k_50k'
            ELSE 'sopra_50k'
        END AS classe_popolazione
    FROM clean_input
    WHERE popolazione > 0 AND percentuale_rd IS NOT NULL
)
SELECT
    anno,
    classe_popolazione,
    regione,
    provincia,
    comune,
    codice_comune_istat,
    popolazione,
    percentuale_rd,
    kg_ru_procapite,
    ROW_NUMBER() OVER (PARTITION BY anno, classe_popolazione ORDER BY percentuale_rd DESC) AS rank_nazionale
FROM comuni_con_classi
ORDER BY anno DESC, classe_popolazione, rank_nazionale
