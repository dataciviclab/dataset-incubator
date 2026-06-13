WITH ricorsi_per_gruppo AS (
    SELECT
        anno,
        codice_sede,
        nome_sede,
        classificazione_ricorso,
        COUNT(DISTINCT numero_ricorso) AS totale_ricorsi
    FROM clean_input
    GROUP BY anno, codice_sede, nome_sede, classificazione_ricorso
),
gare_per_gruppo AS (
    SELECT
        anno,
        codice_sede,
        nome_sede,
        classificazione_ricorso,
        COUNT(DISTINCT numero_gara) AS gare_distinte
    FROM clean_input
    WHERE numero_gara IS NOT NULL AND numero_gara != ''
    GROUP BY anno, codice_sede, nome_sede, classificazione_ricorso
)
SELECT
    r.anno,
    r.codice_sede,
    r.nome_sede,
    r.classificazione_ricorso,
    r.totale_ricorsi,
    COALESCE(g.gare_distinte, 0) AS gare_distinte
FROM ricorsi_per_gruppo r
LEFT JOIN gare_per_gruppo g
    ON r.anno = g.anno
    AND r.codice_sede = g.codice_sede
    AND r.nome_sede = g.nome_sede
    AND r.classificazione_ricorso = g.classificazione_ricorso
ORDER BY r.anno DESC, r.totale_ricorsi DESC
