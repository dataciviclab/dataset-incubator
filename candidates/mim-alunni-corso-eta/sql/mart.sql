WITH scuole AS (
    SELECT *
    FROM read_parquet('{support.scu_anagrafica_statali.mart}')
),
alunni AS (
    SELECT *
    FROM clean
    WHERE ordine_scuola = 'SCUOLA PRIMARIA'
)
SELECT
    a.anno_scolastico,
    s.area_geografica,
    s.regione,
    s.provincia,
    s.codice_comune_scuola,
    s.comune,
    COUNT(DISTINCT a.codice_scuola) AS scuole_osservate,
    SUM(a.alunni) AS alunni_totali
FROM alunni a
LEFT JOIN scuole s
    ON a.codice_scuola = s.codice_scuola
GROUP BY
    a.anno_scolastico,
    s.area_geografica,
    s.regione,
    s.provincia,
    s.codice_comune_scuola,
    s.comune
