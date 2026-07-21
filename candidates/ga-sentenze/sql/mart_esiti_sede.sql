SELECT
    anno,
    codice_sede,
    nome_sede,
    esito_provvedimento,
    COUNT(*) AS totale,
    COUNT(DISTINCT numero_ricorso) AS ricorsi_distinti
FROM clean_input
WHERE esito_provvedimento IS NOT NULL
GROUP BY anno, codice_sede, nome_sede, esito_provvedimento
ORDER BY anno, nome_sede, totale DESC
