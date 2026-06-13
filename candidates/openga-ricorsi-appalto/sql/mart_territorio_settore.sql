SELECT
    anno,
    provincia,
    settore,
    COUNT(*) AS totale_ricorsi,
    SUM(importo_complessivo_gara) AS importo_complessivo_totale,
    COUNT(DISTINCT denominazione_amministrazione_appaltante) AS stazioni_appaltanti_distinte
FROM clean_input
WHERE provincia IS NOT NULL AND provincia != ''
GROUP BY anno, provincia, settore
ORDER BY anno DESC, totale_ricorsi DESC
