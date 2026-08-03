-- mart_trend_anno — Costo PA per rappresentanti nelle partecipate, per anno (multi-year)
--
-- 1 riga = 1 anno: incarichi totali, rappresentanti distinti, spesa totale,
-- quota gratuiti, importo medio, riversato all'amministrazione.
-- Risponde: quanto costa alla PA? (D1 discussion #406)
--
-- PK: (anno)

WITH per_anno AS (
    SELECT
        anno,
        count(*)                                                       AS n_incarichi,
        count(DISTINCT rapp_id)                                        AS n_rappresentanti,
        sum(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL) AS spesa_totale_eur,
        count(*) FILTER (WHERE incarico_gratuito = 'INCARICO GRATUITO') AS n_gratuiti,
        sum(incarico_riversato_eur) FILTER (WHERE incarico_riversato_eur IS NOT NULL) AS riversato_totale_eur,
        round(avg(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL), 0) AS importo_medio_eur
    FROM clean_input
    GROUP BY anno
)
SELECT
    anno,
    n_incarichi,
    n_rappresentanti,
    spesa_totale_eur,
    n_gratuiti,
    round(100.0 * n_gratuiti / NULLIF(n_incarichi, 0), 1)             AS quota_gratuiti_pct,
    importo_medio_eur,
    riversato_totale_eur,
    spesa_totale_eur - lag(spesa_totale_eur) OVER (ORDER BY anno)     AS delta_spesa_eur,
    round(100.0 * (spesa_totale_eur - lag(spesa_totale_eur) OVER (ORDER BY anno))
          / NULLIF(lag(spesa_totale_eur) OVER (ORDER BY anno), 0), 2)  AS variazione_spesa_pct
FROM per_anno
ORDER BY anno
