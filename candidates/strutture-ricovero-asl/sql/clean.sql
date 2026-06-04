-- clean.sql — strutture-ricovero-asl (raw-faithful, conversione separatore migliaia)
-- Il CSV usa "." come separatore migliaia (es. "1.385" = 1385)
-- Lettura con tutte le colonne VARCHAR, conversione manuale

SELECT
    CAST(anno AS INTEGER) AS anno,
    TRIM(codice_struttura) AS codice_struttura,
    TRIM(denominazione_struttura) AS denominazione_struttura,
    TRIM(comune) AS comune,
    TRIM(sigla_provincia_struttura) AS sigla_provincia_struttura,
    CAST(REPLACE(posti_letto_previsti, '.', '') AS INTEGER) AS posti_letto_previsti,
    CAST(REPLACE(posti_letto_utilizzati, '.', '') AS INTEGER) AS posti_letto_utilizzati,
    CAST(REPLACE(personale_uomini, '.', '') AS INTEGER) AS personale_uomini,
    CAST(REPLACE(personale_donne, '.', '') AS INTEGER) AS personale_donne,
    CAST(REPLACE(totale_personale, '.', '') AS INTEGER) AS totale_personale,
    CAST(REPLACE(medici_uomini, '.', '') AS INTEGER) AS medici_uomini,
    CAST(REPLACE(medici_donne, '.', '') AS INTEGER) AS medici_donne,
    CAST(REPLACE(medici, '.', '') AS INTEGER) AS medici,
    CAST(REPLACE(infermieri_uomini, '.', '') AS INTEGER) AS infermieri_uomini,
    CAST(REPLACE(infermieri_donne, '.', '') AS INTEGER) AS infermieri_donne,
    CAST(REPLACE(infermieri, '.', '') AS INTEGER) AS infermieri,
    CAST(REPLACE(ricoveri, '.', '') AS INTEGER) AS ricoveri,
    CAST(REPLACE(giornate_degenza, '.', '') AS INTEGER) AS giornate_degenza,
    CAST(REPLACE(giornate_disponibili, '.', '') AS INTEGER) AS giornate_disponibili,
    CAST(codice_tipo_struttura AS INTEGER) AS codice_tipo_struttura,
    CAST("Sottotipo struttura" AS INTEGER) AS sottotipo_struttura,
    TRIM("Tipo struttura") AS tipo_struttura,
    TRIM(codice_regione) AS codice_regione,
    TRIM("Regione") AS regione,
    CAST(REPLACE(codice_asl, '.', '') AS INTEGER) AS codice_asl,
    TRIM(asl) AS asl
FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
