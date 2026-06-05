-- clean.sql — strutture-ricovero-asl (raw-faithful)
-- Il CSV usa "." come separatore migliaia — gestito da DuckDB
-- tramite read.decimal_separator + read.thousands nel dataset.yml

SELECT
    anno AS anno,
    TRIM(codice_struttura) AS codice_struttura,
    TRIM(denominazione_struttura) AS denominazione_struttura,
    TRIM(comune) AS comune,
    TRIM(sigla_provincia_struttura) AS sigla_provincia_struttura,
    posti_letto_previsti AS posti_letto_previsti,
    posti_letto_utilizzati AS posti_letto_utilizzati,
    personale_uomini AS personale_uomini,
    personale_donne AS personale_donne,
    totale_personale AS totale_personale,
    medici_uomini AS medici_uomini,
    medici_donne AS medici_donne,
    medici AS medici,
    infermieri_uomini AS infermieri_uomini,
    infermieri_donne AS infermieri_donne,
    infermieri AS infermieri,
    ricoveri AS ricoveri,
    giornate_degenza AS giornate_degenza,
    giornate_disponibili AS giornate_disponibili,
    codice_tipo_struttura AS codice_tipo_struttura,
    CAST("Sottotipo struttura" AS INTEGER) AS sottotipo_struttura,
    TRIM("Tipo struttura") AS tipo_struttura,
    TRIM(codice_regione) AS codice_regione,
    TRIM("Regione") AS regione,
    codice_asl AS codice_asl,
    TRIM(asl) AS asl
FROM raw_input
WHERE anno = {year}
