-- clean.sql — mortalita_istat_evitabile
-- Input:  data_base_2022.xlsx, foglio d_base_2022 — ISTAT mortalità per causa
--         granularità: regione × causa × sesso × classe età × titolo di studio
-- Output: righe per regioni italiane (escluse ripartizioni e totale ITALIA),
--         colonne rinominate snake_case, anno = {year}
--
-- Codici territorio:
--   01–22  → regioni e province autonome  ← tenere
--   04     → Trentino-Alto Adige (aggregato delle due PA) ← escludere:
--            21 (Bolzano) e 22 (Trento) sono gia presenti come righe separate,
--            includerlo causerebbe doppio conteggio nel join con le fonti Ministero
--   25     → ITALIA (totale nazionale)    ← escludere
--   31–35  → ripartizioni geografiche     ← escludere

SELECT
    CAST(anno AS INTEGER)                              AS anno,
    TRIM(CAST("Cod_Territorio" AS VARCHAR))            AS cod_territorio,
    TRIM("Territorio")                                 AS territorio,
    CAST("Cod_Sesso" AS INTEGER)                       AS cod_sesso,
    TRIM("Sesso")                                      AS sesso,
    CAST("Cod_Classe età" AS INTEGER)                  AS cod_classe_eta,
    TRIM("Classe età")                                 AS classe_eta,
    CAST("Cod_Titolo di studio" AS INTEGER)            AS cod_titolo_studio,
    TRIM("Titolo di studio")                           AS titolo_studio,
    CAST("Cod_Causa" AS INTEGER)                       AS cod_causa,
    TRIM("Causa")                                      AS causa,
    CAST("pop media" AS DOUBLE)                        AS pop_media,
    CAST("decessi" AS INTEGER)                         AS decessi,
    CAST("tassi_standardizzati per 10.000" AS DOUBLE)  AS tasso_std_10000
FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
  AND CAST("Cod_Territorio" AS INTEGER) BETWEEN 1 AND 22
  AND CAST("Cod_Territorio" AS INTEGER) <> 4
