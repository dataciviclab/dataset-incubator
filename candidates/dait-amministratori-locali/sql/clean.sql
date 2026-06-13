-- Clean: dait_amministratori_locali
-- Fonte: ammcom.csv (DAIT — Ministero dell'Interno)
-- Skip 2 righe di metadati gestito in dataset.yml (clean.read.skip: 2)
-- Encoding UTF-8, delim ; , header letto da riga 3 del CSV
-- Date in formato DD/MM/YYYY — parsate da DuckDB via clean.read.dateformat
--
-- Colonna "lista_appartenenza/collegamento" rinominata in SQL
--
-- Codici territoriali (codice_regione/provincia/comune) mantenuti come VARCHAR
-- per preservare il leading zero. La chiave ISTAT completa e':
--   codice_regione (2) || codice_provincia (3) || codice_comune (3) = 8 char
-- Il cast a INTEGER perderebbe il padding, rendendo impossibile il join
-- con dataset ISTAT o BDAP.

SELECT
    {year}::INTEGER                                       AS anno,
    NULLIF(codice_regione, '')                            AS codice_regione,
    NULLIF(codice_provincia, '')                          AS codice_provincia,
    NULLIF(codice_comune, '')                             AS codice_comune,
    NULLIF(codice_regione || codice_provincia || codice_comune, '')
                                                          AS codice_completo,
    denominazione_comune                                  AS denominazione_comune,
    sigla_provincia                                       AS sigla_provincia,
    NULLIF(popolazione_censita_alla_data_elezione, '')::INTEGER
                                                          AS popolazione_censita,
    cognome                                               AS cognome,
    nome                                                  AS nome,
    sesso                                                 AS sesso,
    data_nascita                                          AS data_nascita,
    luogo_nascita                                         AS luogo_nascita,
    descrizione_carica                                    AS descrizione_carica,
    NULLIF(incarico, '')                                  AS incarico,
    data_elezione                                         AS data_elezione,
    data_entrata_in_carica                                AS data_entrata_in_carica,
    NULLIF("lista_appartenenza/collegamento", '')         AS lista_appartenenza,
    NULLIF(titolo_studio, '')                             AS titolo_studio,
    NULLIF(professione, '')                               AS professione
FROM raw_input
