SELECT
    anno,
    codice_sede,
    nome_sede,
    classificazione_ricorso,
    COUNT(*) AS totale_ricorsi,
    COUNT(DISTINCT codice_cig) AS gare_distinte,
    SUM(importo_complessivo_gara) AS importo_complessivo_totale,
    AVG(importo_complessivo_gara) AS importo_medio_gara
FROM clean_input
GROUP BY anno, codice_sede, nome_sede, classificazione_ricorso
ORDER BY anno DESC, totale_ricorsi DESC
