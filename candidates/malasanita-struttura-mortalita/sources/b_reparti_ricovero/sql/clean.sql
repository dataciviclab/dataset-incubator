-- clean.sql — malasanita_b_reparti_ricovero
-- Input:  reparti_ricovero_2022.csv (granularità: reparto/struttura)
-- Output: una riga per reparto, colonne selezionate snake_case, anno = {{year}}
-- Nota:   degenza_media_ordinaria, icm, tasso_utilizzo usano virgola come decimale
--         num_dimessi e giornate_* usano punto come separatore migliaia → restano VARCHAR

SELECT
    CAST(anno AS INTEGER)              AS anno,
    TRIM(CAST(codice_regione AS VARCHAR)) AS codice_regione,
    TRIM(regione)                      AS regione,
    TRIM(CAST(codice_asl AS VARCHAR))  AS codice_asl,
    TRIM(asl)                          AS asl,
    TRIM(CAST(codice_struttura AS VARCHAR)) AS codice_struttura,
    TRIM(struttura)                    AS struttura,
    TRIM(codice_disciplina)            AS codice_disciplina,
    TRIM(disciplina)                   AS disciplina,
    CAST(posti_letto_day_hospital AS INTEGER)       AS posti_letto_day_hospital,
    CAST(posti_letto_day_surgery AS INTEGER)        AS posti_letto_day_surgery,
    CAST(posti_letto_degenza_ordinaria AS INTEGER)  AS posti_letto_degenza_ordinaria,
    CAST(posti_letto_utilizzati AS INTEGER)         AS posti_letto_utilizzati,
    num_dimessi                        AS num_dimessi_raw,
    giornate_degenza                   AS giornate_degenza_raw

FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
