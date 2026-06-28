-- Mart: bambini scuola infanzia — arricchiti per territorio
SELECT
    anno_scolastico,
    codice_scuola,
    denominazione_scuola,
    grado_istruzione_scuola,
    caratteristica_scuola,
    bambini_italiani,
    bambini_non_italiani,
    bambini_totale,
    area_geografica,
    regione,
    provincia,
    comune,
    codice_comune_scuola,
    denominazione_istituto_riferimento
FROM clean_input
