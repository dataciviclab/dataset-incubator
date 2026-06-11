-- Clean: dait_amministratori_locali
-- Fonte: ammcom.csv (DAIT — Ministero dell'Interno)
-- Skip 2 righe di metadati gestito in dataset.yml (clean.read.skip: 2)
-- Encoding UTF-8, delim ; , header letto da riga 3 del CSV
-- all_varchar: true in dataset.yml — tutti i cast sono espliciti in SQL
--
-- Colonna "lista_appartenenza/collegamento" rinominata in SQL
-- Date in formato DD/MM/YYYY — mantenute come testo in clean (raw-faithful)

SELECT
    {year}::INTEGER                                       AS anno,
    NULLIF(codice_regione, '')::INTEGER                   AS codice_regione,
    NULLIF(codice_provincia, '')::INTEGER                 AS codice_provincia,
    NULLIF(codice_comune, '')::INTEGER                    AS codice_comune,
    denominazione_comune                                  AS denominazione_comune,
    sigla_provincia                                       AS sigla_provincia,
    NULLIF(popolazione_censita_alla_data_elezione, '')::INTEGER
                                                          AS popolazione_censita,
    cognome                                               AS cognome,
    nome                                                  AS nome,
    sesso                                                 AS sesso,
    NULLIF(data_nascita, '')                              AS data_nascita,
    luogo_nascita                                         AS luogo_nascita,
    descrizione_carica                                    AS descrizione_carica,
    NULLIF(incarico, '')                                  AS incarico,
    NULLIF(data_elezione, '')                             AS data_elezione,
    NULLIF(data_entrata_in_carica, '')                    AS data_entrata_in_carica,
    NULLIF("lista_appartenenza/collegamento", '')         AS lista_appartenenza,
    NULLIF(titolo_studio, '')                             AS titolo_studio,
    NULLIF(professione, '')                               AS professione
FROM raw_input
