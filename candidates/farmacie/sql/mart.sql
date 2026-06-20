-- Farmacie: conteggio per comune, tipologia, provincia
-- Snapshot corrente (2026)

-- mart: farmacie per comune
SELECT
    cod_comune,
    comune,
    sigla_provincia,
    provincia,
    cod_regione,
    regione,
    codice_tipologia,
    descrizione_tipologia,
    count(*) AS n_farmacie
FROM clean_input
GROUP BY
    cod_comune, comune, sigla_provincia, provincia,
    cod_regione, regione,
    codice_tipologia, descrizione_tipologia
ORDER BY n_farmacie DESC
