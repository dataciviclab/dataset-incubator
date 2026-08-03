-- mart_gender_gap — Divario di genere nei compensi per anno
--
-- 1 riga = 1 (anno, genere): incarichi remunerati, importo medio, spesa
-- totale, quota incarichi. Risponde: quanto è profondo il divario di
-- genere? (D3 discussion #406). Il confronto M/F va fatto a valle
-- (ratio importo medio), oppure con join self — qui esponiamo i dati
-- grezzi per anno per calcolare il gap senza ambiguità.
--
-- PK: (anno, rapp_genere)

SELECT
    anno,
    rapp_genere,
    count(*) FILTER (WHERE incarico_gratuito = 'INCARICO REMUNERATO') AS n_remunerati,
    round(avg(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL), 0) AS importo_medio_eur,
    sum(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL) AS spesa_totale_eur,
    round(100.0 * count(*) FILTER (WHERE incarico_gratuito = 'INCARICO REMUNERATO')
          / NULLIF(count(*) FILTER (WHERE rapp_genere IS NOT NULL), 0), 1) AS quota_remunerati_pct
FROM clean_input
WHERE rapp_genere IS NOT NULL
GROUP BY anno, rapp_genere
ORDER BY anno, rapp_genere
