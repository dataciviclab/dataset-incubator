WITH ricorsi_per_gruppo AS (
    SELECT
        anno,
        provincia,
        COALESCE(settore, 'ND') AS settore,
        COUNT(DISTINCT numero_ricorso) AS totale_ricorsi
    FROM clean_input
    WHERE provincia IS NOT NULL AND provincia != ''
    GROUP BY anno, provincia, COALESCE(settore, 'ND')
),
gare_per_gruppo AS (
    SELECT
        anno,
        provincia,
        COALESCE(settore, 'ND') AS settore,
        COUNT(DISTINCT numero_gara) AS gare_distinte
    FROM clean_input
    WHERE provincia IS NOT NULL AND provincia != ''
      AND numero_gara IS NOT NULL AND numero_gara != ''
    GROUP BY anno, provincia, COALESCE(settore, 'ND')
)
SELECT
    r.anno,
    r.provincia,
    r.settore,
    r.totale_ricorsi,
    COALESCE(g.gare_distinte, 0) AS gare_distinte
FROM ricorsi_per_gruppo r
LEFT JOIN gare_per_gruppo g
    ON r.anno = g.anno
    AND r.provincia = g.provincia
    AND r.settore = g.settore
ORDER BY r.anno DESC, r.totale_ricorsi DESC
