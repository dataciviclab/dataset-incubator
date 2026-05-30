-- Clean: alunni per corso/eta + join anagrafica scuole
-- Arricchisce ogni record alunno con i metadati della scuola (regione, provincia, comune, ecc.)
WITH alunni AS (
    SELECT
        CAST(ANNOSCOLASTICO AS VARCHAR) AS anno_scolastico,
        TRIM(CODICESCUOLA) AS codice_scuola,
        TRIM(ORDINESCUOLA) AS ordine_scuola,
        CAST(ANNOCORSO AS VARCHAR) AS anno_corso,
        TRIM(FASCIAETA) AS fascia_eta,
        TRY_CAST(ALUNNI AS BIGINT) AS alunni
    FROM raw_input
    WHERE CODICESCUOLA IS NOT NULL
      AND TRY_CAST(ALUNNI AS BIGINT) IS NOT NULL
),
scuole AS (
    SELECT *
    FROM read_parquet('{support.scu_anagrafica_statali.mart}')
)
SELECT
    a.anno_scolastico,
    a.codice_scuola,
    s.denominazione_scuola,
    a.ordine_scuola,
    s.grado_istruzione_scuola,
    s.caratteristica_scuola,
    a.anno_corso,
    a.fascia_eta,
    a.alunni,
    s.area_geografica,
    s.regione,
    s.provincia,
    s.comune,
    s.codice_comune_scuola,
    s.cap_scuola,
    s.denominazione_istituto_riferimento
FROM alunni a
LEFT JOIN scuole s ON a.codice_scuola = s.codice_scuola
