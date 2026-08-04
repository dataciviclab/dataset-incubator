-- clean.sql — senato_ddl
--
-- Iter legislativo dei disegni di legge del Senato (XIX legislatura).
-- Input: 3 sorgenti SPARQL (q1, q2a, q2b) unite con union_by_name via
-- read.mode: all — ogni sorgente ha un sottoinsieme di colonne (il WAF
-- Senato rifiuta query > ~15 colonne). L'unione produce 3 righe per ddl
-- (una per sorgente) con colonne vuote per quelle non presenti.
-- Qui ricombiniamo con GROUP BY ddl + MAX.
--
-- Filtro: teniamo SOLO gli URI /ddl/N (con metadati); /iterDdl/N sono
-- l'iter (metadati vuoti). Il WAF rifiuta CONTAINS in query → filtro qui.
--
-- Nota: il plugin SPARQL scrive CSV non quotato → read_mode: robust.

SELECT
    -- id numerico del ddl
    MAX(TRY_CAST(
        CASE WHEN idDdl IS NOT NULL
             THEN regexp_extract(CAST(idDdl AS VARCHAR), '(\d+)', 1)
        END AS BIGINT
    ))                                                                AS id_ddl,
    MAX(normalize_string(ddl))                                        AS ddl_url,
    MAX(normalize_string(titolo))                                     AS titolo,
    MAX(normalize_string(titoloBreve))                                AS titolo_breve,
    MAX(normalize_string(stato))                                      AS stato,
    MAX(TRY_CAST(dataPresentazione AS DATE))                          AS data_presentazione,
    MAX(TRY_CAST(dataStatoDdl AS DATE))                               AS data_stato_ddl,
    MAX(normalize_string(natura))                                     AS natura,
    -- fase: codice atto (C.1774 = Camera, S.782 = Senato); blank node esclusi
    MAX(CASE WHEN fase LIKE 'nodeID://%' OR fase IS NULL THEN NULL
             ELSE normalize_string(fase)
        END)                                                          AS fase,
    MAX(normalize_string(ramo))                                       AS ramo,
    -- iniziativa: URI → codice finale (es. INIZ-DDL-...)
    MAX(CASE
            WHEN iniziativa LIKE '%/iniziativa/%' THEN
                substring(iniziativa, strpos(iniziativa, '/iniziativa/') + 12)
            ELSE normalize_string(iniziativa)
        END)                                                          AS iniziativa,
    MAX(normalize_string(descrIniziativa))                            AS descr_iniziativa,
    MAX(TRY_CAST(CAST(progressivoIter AS VARCHAR) AS BIGINT))         AS progressivo_iter,
    MAX(TRY_CAST(CAST(numeroFase AS VARCHAR) AS BIGINT))              AS numero_fase,
    MAX(normalize_string(numeroFaseCompatto))                         AS numero_fase_compatto,
    MAX(normalize_string(idFase))                                     AS id_fase,
    MAX(TRY_CAST(CAST(legislatura AS VARCHAR) AS BIGINT))             AS legislatura,
    MAX(normalize_string(presentatoTrasmesso))                        AS presentato_trasmesso,
    MAX(TRY_CAST(CAST(numeroLegge AS VARCHAR) AS BIGINT))             AS numero_legge,
    MAX(TRY_CAST(dataLegge AS DATE))                                  AS data_legge,
    MAX(normalize_string(relatore))                                   AS relatore,
    MAX(normalize_string(classificazione))                            AS classificazione,
    MAX(normalize_string(assegnazione))                               AS assegnazione,
    MAX(normalize_string(testoPresentato))                            AS testo_presentato,
    MAX(normalize_string(testoApprovato))                             AS testo_approvato,
    MAX(normalize_string(testoUnificato))                             AS testo_unificato,
    MAX(normalize_string(stralcio))                                   AS stralcio
FROM raw_input
WHERE ddl LIKE '%/ddl/%'
GROUP BY ddl
