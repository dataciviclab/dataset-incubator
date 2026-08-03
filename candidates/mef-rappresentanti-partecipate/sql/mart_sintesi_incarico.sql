-- mart_sintesi_incarico — Compensi per tipo di incarico e anno
--
-- 1 riga = 1 (anno, tipo incarico): incarichi remunerati, importo medio,
-- importo massimo, spesa totale. Risponde: chi prende di più per ruolo?
-- AD vs consigliere (D2), liquidatori (D11 discussion #406).
--
-- PK: (anno, incarico_tipo)

SELECT
    anno,
    incarico_tipo,
    count(*) FILTER (WHERE incarico_gratuito = 'INCARICO REMUNERATO') AS n_remunerati,
    round(avg(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL), 0) AS importo_medio_eur,
    max(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL) AS importo_max_eur,
    sum(incarico_importo_eur) FILTER (WHERE incarico_importo_eur IS NOT NULL) AS spesa_totale_eur
FROM clean_input
WHERE incarico_tipo IS NOT NULL
GROUP BY anno, incarico_tipo
ORDER BY anno, importo_medio_eur DESC
