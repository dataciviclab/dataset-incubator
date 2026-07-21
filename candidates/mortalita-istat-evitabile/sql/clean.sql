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
    normalize_string("Cod_Territorio")            AS cod_territorio,
    normalize_string("Territorio")                                 AS territorio,
    cast_int("Cod_Sesso")                       AS cod_sesso,
    normalize_string("Sesso")                                      AS sesso,
    cast_int("Cod_Classe età")                  AS cod_classe_eta,
    normalize_string("Classe età")                                 AS classe_eta,
    cast_int("Cod_Titolo di studio")            AS cod_titolo_studio,
    normalize_string("Titolo di studio")                           AS titolo_studio,
    cast_int("Cod_Causa")                       AS cod_causa,
    normalize_string("Causa")                                      AS causa,
    cast_double("pop media")                        AS pop_media,
    cast_int("decessi")                         AS decessi,
    cast_double("tassi_standardizzati per 10.000")  AS tasso_std_10000
FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
  AND cast_int("Cod_Territorio") BETWEEN 1 AND 22
  AND cast_int("Cod_Territorio") <> 4
