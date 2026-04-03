SELECT
    CAST(ANNOSCOLASTICO AS VARCHAR) AS anno_scolastico,
    TRIM(CODICESCUOLA) AS codice_scuola,
    TRIM(CODICEISTITUTORIFERIMENTO) AS codice_istituto_riferimento,
    TRIM(DENOMINAZIONEISTITUTORIFERIMENTO) AS denominazione_istituto_riferimento,
    TRIM(DENOMINAZIONESCUOLA) AS denominazione_scuola,
    TRIM(AREAGEOGRAFICA) AS area_geografica,
    TRIM(REGIONE) AS regione,
    TRIM(PROVINCIA) AS provincia,
    TRIM(CODICECOMUNESCUOLA) AS codice_comune_scuola,
    TRIM(DESCRIZIONECOMUNE) AS comune,
    TRIM(CAPSCUOLA) AS cap_scuola,
    TRIM(INDIRIZZOSCUOLA) AS indirizzo_scuola,
    TRIM(DESCRIZIONECARATTERISTICASCUOLA) AS caratteristica_scuola,
    TRIM(DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA) AS grado_istruzione_scuola
FROM raw_input
WHERE CODICESCUOLA IS NOT NULL
