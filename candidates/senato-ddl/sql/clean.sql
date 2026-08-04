-- clean.sql — senato_ddl
--
-- Iter legislativo dei disegni di legge del Senato (XIX legislatura).
-- Input: CSV da endpoint SPARQL dati.senato.it (una riga = un ddl, già
-- deduplicato con GROUP BY + MAX lato query).
--
-- Filtro chiave: l'endpoint espone ogni ddl in DUE forme — URI /ddl/N
-- (con metadati: titolo, stato, data) e URI /iterDdl/N (solo l'iter,
-- metadati vuoti). Teniamo SOLO /ddl/N. Il WAF Senato rifiuta CONTAINS
-- in query con GROUP BY → il filtro si fa qui nel clean, non nella query.
--
-- Nota: il plugin SPARQL scrive CSV non quotato → read_mode: robust
-- (apostrofi nei titoli, es. "Modifica all'articolo").

SELECT
    -- id numerico del ddl
    TRY_CAST(
        CASE WHEN idDdl IS NOT NULL
             THEN regexp_extract(CAST(idDdl AS VARCHAR), '(\d+)', 1)
        END AS BIGINT
    )                                                                 AS id_ddl,
    normalize_string(ddl)                                             AS ddl_url,
    normalize_string(titolo)                                          AS titolo,
    normalize_string(stato)                                           AS stato,
    TRY_CAST(data AS DATE)                                            AS data_presentazione,
    normalize_string(tipo)                                            AS tipo_iniziativa,
    -- fase: codice atto (es. C.1774 = atto Camera, S.782 = Senato).
    -- Esclude solo i blank node (nodeID://) — NON richiedere URL.
    CASE WHEN fase LIKE 'nodeID://%' OR fase IS NULL THEN NULL
         ELSE normalize_string(fase)
    END                                                               AS fase
FROM raw_input
WHERE ddl LIKE '%/ddl/%'
  AND idDdl IS NOT NULL
