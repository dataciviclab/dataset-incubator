-- mart_gruppi_legislatura — gruppi parlamentari per legislatura
--
-- 1 riga = 1 legislatura: numero di gruppi parlamentari attivi.
-- Risponde: quanti gruppi per legislatura? (per dare il nome ai gruppi di
-- camera_incarichi, che oggi espone solo l'URI)
--
-- PK: (legislatura)

SELECT
    legislatura,
    count(*) AS n_gruppi
FROM clean_input
WHERE legislatura IS NOT NULL
GROUP BY legislatura
ORDER BY legislatura
