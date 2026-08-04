-- clean.sql — senato_firmatari
--
-- Firmatari/presentatori dei ddl del Senato (XIX legislatura, graph ddl/19).
-- La fonte espone i firmatari come risorse osr:iniziativa collegate al ddl:
--   ddl --osr:iniziativa--> iniziativa/* --osr:presentatore--> "Sen. Mario Turco"
--                                      --osr:primoFirmatario--> "1"
--                                      --osr:tipoIniziativa--> "Parlamentare"
--                                      --osr:senatore--> URI senatore (se senatore)
--
-- Nota: non tutti i firmatari hanno osr:senatore (i presentatori "On." deputati
-- o "Ministro" governativi non hanno URL senatore). primoFirmatario è presente
-- su ~16% delle iniziative (il resto è "ed altri" non espanso in risorse).

WITH base AS (
    SELECT * FROM raw_input
)
SELECT
    normalize_string(ddl)                                             AS ddl,
    -- id del ddl: usa osr:idDdl (numerazione interna condivisa con
    -- senato-ddl) — NON l'id dall'URI /ddl/N che è una numerazione diversa
    TRY_CAST(idDdl AS BIGINT)                                         AS ddl_id,
    normalize_string(iniziativa)                                      AS iniziativa,
    normalize_string(presentatore)                                    AS presentatore,
    normalize_string(tipoIniziativa)                                  AS tipo_iniziativa,
    -- primoFirmatario: "1"/"0" (o NULL se assente) → BOOLEAN
    TRY_CAST(primoFirmatario AS BOOLEAN)                              AS primo_firmatario,
    -- id numerico del senatore dall'URI /senatore/N (NULL per non-senatori)
    TRY_CAST(regexp_extract(senatore, '/senatore/(\d+)', 1) AS BIGINT) AS senatore_id,
    -- data aggiunta firma: la fonte la fornisce già in formato ISO (es. 2023-05-26)
    TRY_CAST(dataAggiuntaFirma AS DATE)                               AS data_aggiunta_firma,
    -- data ritiro firma: stesso formato ISO (NULL = firma ancora valida)
    TRY_CAST(dataRitiroFirma AS DATE)                                 AS data_ritiro_firma,
    -- URI deputato Camera (presentatori 'On.' — NULL per senatori/governativi)
    normalize_string(deputato)                                        AS deputato_url
FROM base
WHERE ddl IS NOT NULL
  AND presentatore IS NOT NULL
