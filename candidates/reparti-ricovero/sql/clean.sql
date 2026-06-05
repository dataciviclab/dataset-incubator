-- clean.sql — reparti-ricovero (raw-faithful)
-- Nota: num_dimessi e giornate_degenza hanno separatore migliaia (es. "2.433")
--       → restano VARCHAR per non perdere informazione

SELECT
    CAST(anno AS INTEGER) AS anno,
    TRIM(CAST(codice_regione AS VARCHAR)) AS codice_regione,
    TRIM(regione) AS regione,
    TRIM(CAST(codice_asl AS VARCHAR)) AS codice_asl,
    TRIM(asl) AS asl,
    TRIM(CAST(codice_struttura AS VARCHAR)) AS codice_struttura,
    TRIM(struttura) AS struttura,
    TRIM(indirizzo) AS indirizzo,
    CAST(codice_tipo_struttura AS INTEGER) AS codice_tipo_struttura,
    CAST(sottotipo_struttura AS INTEGER) AS sottotipo_struttura,
    TRIM(tipo_struttura) AS tipo_struttura,
    TRIM(comune) AS comune,
    TRIM(sigla_provincia) AS sigla_provincia,
    TRIM(CAST(codice_disciplina AS VARCHAR)) AS codice_disciplina,
    TRIM(disciplina) AS disciplina,
    CAST(posti_letto_day_hospital AS INTEGER) AS posti_letto_day_hospital,
    CAST(posti_letto_day_surgery AS INTEGER) AS posti_letto_day_surgery,
    CAST(posti_letto_degenza_ordinaria AS INTEGER) AS posti_letto_degenza_ordinaria,
    CAST(posti_letto_utilizzati AS INTEGER) AS posti_letto_utilizzati,
    CAST(num_dimessi AS VARCHAR) AS num_dimessi,
    CAST(giornate_degenza AS VARCHAR) AS giornate_degenza,
    CAST(giornate_disponibili AS DOUBLE) AS giornate_disponibili,
    CAST(degenza_media_ordinaria AS DOUBLE) AS degenza_media_ordinaria,
    CAST(icm AS DOUBLE) AS icm,
    CAST(tasso_utilizzo AS DOUBLE) AS tasso_utilizzo
FROM raw_input
WHERE CAST(anno AS INTEGER) = {year}
