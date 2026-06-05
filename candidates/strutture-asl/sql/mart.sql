-- mart.sql - strutture_asl - mart_regioni
-- Output: una riga per regione / PA con personale territoriale e residenti

SELECT
    anno,
    codice_regione,
    regione,
    SUM(totale_medici) AS medici_mmg,
    SUM(totale_pediatri) AS pediatri,
    SUM(totale_residenti) AS pop_residente,
    ROUND(SUM(totale_medici) * 100000.0 / NULLIF(SUM(totale_residenti), 0), 2) AS medici_mmg_per_100k,
    ROUND(SUM(totale_pediatri) * 100000.0 / NULLIF(SUM(totale_residenti), 0), 2) AS pediatri_per_100k
FROM clean_input
GROUP BY anno, codice_regione, regione
ORDER BY codice_regione
