WITH ricorsi AS (
    SELECT DISTINCT numero_ricorso, anno, provincia, settore
    FROM clean_input
    WHERE provincia IS NOT NULL AND provincia != ''
),
gare_per_gruppo AS (
    SELECT DISTINCT r.anno, r.provincia, r.settore,
           ci.numero_gara
    FROM clean_input ci
    JOIN ricorsi r ON ci.numero_ricorso = r.numero_ricorso AND ci.anno = r.anno
    WHERE ci.numero_gara IS NOT NULL AND ci.numero_gara != ''
)
SELECT
    r.anno,
    r.provincia,
    r.settore,
    COUNT(*) AS totale_ricorsi,
    COUNT(DISTINCT gg.numero_gara) AS gare_distinte
FROM ricorsi r
LEFT JOIN gare_per_gruppo gg ON r.anno = gg.anno 
    AND r.provincia = gg.provincia 
    AND r.settore = gg.settore
GROUP BY r.anno, r.provincia, r.settore
ORDER BY r.anno DESC, totale_ricorsi DESC
