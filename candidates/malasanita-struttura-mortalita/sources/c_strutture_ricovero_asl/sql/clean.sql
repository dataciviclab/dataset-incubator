-- clean.sql — malasanita_c_strutture_ricovero
-- Input:  strutture_ricovero_asl_2022.csv (granularità: struttura)
-- Output: una riga per struttura, colonne rinominate snake_case, anno = {{year}}
-- Nota:   ricoveri e giornate_* usano punto come separatore migliaia → restano VARCHAR

SELECT
    CAST(anno AS INTEGER)                      AS anno,
    TRIM(CAST(codice_struttura AS VARCHAR))    AS codice_struttura,
    TRIM(denominazione_struttura)              AS denominazione_struttura,
    TRIM(CAST(codice_regione AS VARCHAR))      AS codice_regione,
    TRIM("Regione")                            AS regione,
    TRIM(CAST(codice_asl AS VARCHAR))          AS codice_asl,
    TRIM(asl)                                  AS asl,
    CAST(posti_letto_previsti AS INTEGER)      AS posti_letto_previsti,
    CAST(posti_letto_utilizzati AS INTEGER)    AS posti_letto_utilizzati,
    CAST(totale_personale AS INTEGER)          AS totale_personale,
    CAST(medici AS INTEGER)                    AS medici,
    CAST(infermieri AS INTEGER)                AS infermieri,
    ricoveri                                   AS ricoveri_raw,
    giornate_degenza                           AS giornate_degenza_raw

FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
