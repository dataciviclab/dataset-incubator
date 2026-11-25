-- mart_sintesi.sql — AMECO: sintesi per paese × serie
--
-- Una riga per paese × serie con:
--   - ultimo valore osservato disponibile
--   - previsioni ECFIN 2025-2027 (Spring 2026)
--
-- Gruppi: paese × serie → primary_key [paese, serie]

WITH base AS (
    SELECT
        paese,
        paese_nome,
        serie,
        titolo,
        unita,
        anno,
        valore,
        tipo_dato,
        max(CASE WHEN tipo_dato = 'osservato' THEN anno END)
            OVER (PARTITION BY paese, serie) AS anno_ultimo
    FROM clean_input
)
SELECT
    paese,
    paese_nome,
    serie,
    titolo,
    unita,
    anno_ultimo,
    max(CASE WHEN anno = anno_ultimo THEN valore END) AS valore_ultimo,
    max(CASE WHEN anno = 2025 THEN valore END) AS valore_2025,
    max(CASE WHEN anno = 2026 THEN valore END) AS valore_2026,
    max(CASE WHEN anno = 2027 THEN valore END) AS valore_2027
FROM base
GROUP BY paese, paese_nome, serie, titolo, unita, anno_ultimo
ORDER BY paese, serie
