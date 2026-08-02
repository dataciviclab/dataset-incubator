-- Clean: alunni per corso/eta + join anagrafica scuole
-- Arricchisce ogni record alunno con i metadati della scuola (regione,
-- provincia, comune, ecc.) via support mim-anagrafica-scuole-statali.
-- Macro standard: cast_int/cast_bigint/normalize_string.

WITH alunni AS (
    SELECT
        normalize_string(ANNOSCOLASTICO) AS anno_scolastico,
        normalize_string(CODICESCUOLA) AS codice_scuola,
        normalize_string(ORDINESCUOLA) AS ordine_scuola,
        normalize_string(ANNOCORSO) AS anno_corso,
        normalize_string(FASCIAETA) AS fascia_eta,
        cast_bigint(ALUNNI) AS alunni
    FROM raw_input
    WHERE CODICESCUOLA IS NOT NULL
      AND cast_bigint(ALUNNI) IS NOT NULL
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
