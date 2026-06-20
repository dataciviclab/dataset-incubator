-- Mart annuale: ricorsi pendenti per sede e anno
-- Aggrega i valori mensili in indicatori annuali

SELECT
    anno,
    codice_sede,
    nome_sede,
    COUNT(*) AS mesi_con_dato,
    MAX(numero_ricorsi_pendenti) AS max_ricorsi_pendenti,
    MIN(numero_ricorsi_pendenti) AS min_ricorsi_pendenti,
    AVG(numero_ricorsi_pendenti)::BIGINT AS media_ricorsi_pendenti,
    MAX(numero_ricorsi_pendenti) - MIN(numero_ricorsi_pendenti) AS variazione_annuale
FROM clean_input
GROUP BY anno, codice_sede, nome_sede
ORDER BY anno, nome_sede
