-- Clean: bambini scuola infanzia per cittadinanza + join anagrafica scuole
--
-- Input: INFANZIASTRACITSTA da MIM (4 colonne)
-- Arricchisce ogni record scuola con i metadati territoriali (regione, provincia, comune)

WITH bambini AS (
    SELECT
        CAST(ANNOSCOLASTICO AS VARCHAR) AS anno_scolastico,
        TRIM(CODICESCUOLA) AS codice_scuola,
        TRY_CAST(BAMBINICITTADINANZAITALIANA AS INTEGER) AS bambini_italiani,
        TRY_CAST(BAMBINICITTADINANZANONITALIANA AS INTEGER) AS bambini_non_italiani
    FROM raw_input
    WHERE CODICESCUOLA IS NOT NULL
),

scuole AS (
    SELECT *
    FROM read_parquet('{support.scu_anagrafica_statali.mart}')
)

SELECT
    b.anno_scolastico,
    b.codice_scuola,
    s.denominazione_scuola,
    s.grado_istruzione_scuola,
    s.caratteristica_scuola,
    b.bambini_italiani,
    b.bambini_non_italiani,
    (COALESCE(b.bambini_italiani, 0) + COALESCE(b.bambini_non_italiani, 0)) AS bambini_totale,
    s.area_geografica,
    s.regione,
    s.provincia,
    s.comune,
    s.codice_comune_scuola,
    s.denominazione_istituto_riferimento
FROM bambini b
LEFT JOIN scuole s ON b.codice_scuola = s.codice_scuola
