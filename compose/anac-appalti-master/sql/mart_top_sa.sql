-- Top stazioni appaltanti per volume
SELECT
    amministrazione,
    count(*) AS n_bandi,
    round(sum(importo_complessivo_gara), 0) AS importo_totale_bandi,
    round(sum(importo_agg), 0) AS importo_totale_aggiudicato,
    count(DISTINCT operatore) AS n_operatori_distinti,
    round(avg(n_partecipanti), 1) AS media_partecipanti
FROM clean_input
WHERE amministrazione IS NOT NULL
GROUP BY amministrazione
ORDER BY importo_totale_bandi DESC
LIMIT 100
