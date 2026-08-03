-- mart_top_amministrazioni — Amministrazioni con più incarichi e compensi
--
-- 1 riga = 1 (anno, amministrazione): incarichi nominati, rappresentanti
-- distinti, spesa totale, riversato, quota gratuiti. Risponde: quali
-- amministrazioni nominano di più e pagano di più? (D5), quanto viene
-- riversato (D8 discussion #406).
--
-- PK: (anno, amm_cf)

SELECT
    anno,
    amm_cf,
    amministrazione,
    amm_macrocategoria,
    amm_categoria,
    amm_regione,
    count(*)                                                       AS n_incarichi,
    count(DISTINCT rapp_id)                                        AS n_rappresentanti,
    sum(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL) AS spesa_totale_eur,
    sum(incarico_riversato_eur) FILTER (WHERE incarico_riversato_eur IS NOT NULL) AS riversato_totale_eur,
    round(100.0 * count(*) FILTER (WHERE incarico_gratuito = 'INCARICO GRATUITO')
          / NULLIF(count(*), 0), 1)                               AS quota_gratuiti_pct
FROM clean_input
WHERE amm_cf IS NOT NULL
GROUP BY
    anno, amm_cf, amministrazione, amm_macrocategoria,
    amm_categoria, amm_regione
ORDER BY anno, spesa_totale_eur DESC NULLS LAST
