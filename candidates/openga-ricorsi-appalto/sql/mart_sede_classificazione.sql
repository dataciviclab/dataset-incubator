WITH ricorsi AS (
    -- Una riga per ricorso, indipendentemente dai lotti CIG
    SELECT DISTINCT numero_ricorso, anno, codice_sede, nome_sede, classificazione_ricorso
    FROM clean_input
),
gare_per_gruppo AS (
    -- Gare coinvolte in almeno un ricorso del gruppo
    SELECT DISTINCT r.anno, r.codice_sede, r.nome_sede, r.classificazione_ricorso,
           ci.numero_gara
    FROM clean_input ci
    JOIN ricorsi r ON ci.numero_ricorso = r.numero_ricorso AND ci.anno = r.anno
    WHERE ci.numero_gara IS NOT NULL AND ci.numero_gara != ''
)
SELECT
    r.anno,
    r.codice_sede,
    r.nome_sede,
    r.classificazione_ricorso,
    COUNT(*) AS totale_ricorsi,
    COUNT(DISTINCT gg.numero_gara) AS gare_distinte
FROM ricorsi r
LEFT JOIN gare_per_gruppo gg ON r.anno = gg.anno 
    AND r.codice_sede = gg.codice_sede 
    AND r.nome_sede = gg.nome_sede 
    AND r.classificazione_ricorso = gg.classificazione_ricorso
GROUP BY r.anno, r.codice_sede, r.nome_sede, r.classificazione_ricorso
ORDER BY r.anno DESC, totale_ricorsi DESC
