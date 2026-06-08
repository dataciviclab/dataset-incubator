-- Clean: Posti letto per stabilimento ospedaliero e disciplina
-- Fonte: Ministero della Salute — Open Data
-- Periodo: 2020-2023

SELECT
    TRY_CAST("Anno" AS INTEGER) AS anno,
    TRY_CAST("Codice Regione" AS INTEGER) AS codice_regione,
    TRIM("Descrizione Regione") AS descrizione_regione,
    TRY_CAST("Codice Azienda" AS INTEGER) AS codice_azienda,
    TRY_CAST("Tipo Azienda" AS INTEGER) AS tipo_azienda,
    TRY_CAST("Codice struttura" AS INTEGER) AS codice_struttura,
    TRY_CAST("Subcodice" AS INTEGER) AS subcodice,
    TRIM("Denominazione Struttura/Stabilimento") AS denominazione_struttura_stabilimento,
    TRIM("Indirizzo") AS indirizzo,
    TRY_CAST("Codice Comune" AS INTEGER) AS codice_comune,
    TRIM("Comune") AS comune,
    TRIM("Sigla Provincia") AS sigla_provincia,
    TRY_CAST("Codice tipo struttura" AS DOUBLE) AS codice_tipo_struttura,
    TRIM("Descrizione tipo struttura") AS descrizione_tipo_struttura,
    TRY_CAST("Codice disciplina" AS INTEGER) AS codice_disciplina,
    TRIM("Descrizione disciplina") AS descrizione_disciplina,
    TRIM("Tipo di Disciplina") AS tipo_di_disciplina,
    TRY_CAST("N° Reparti" AS INTEGER) AS n_reparti,
    TRY_CAST("Posti letto degenza ordinaria" AS BIGINT) AS posti_letto_degenza_ordinaria,
    TRY_CAST("Posti letto degenza a pagamento" AS BIGINT) AS posti_letto_degenza_a_pagamento,
    TRY_CAST("Posti letto Day Hospital" AS BIGINT) AS posti_letto_day_hospital,
    TRY_CAST("Posti letto Day Surgery" AS BIGINT) AS posti_letto_day_surgery,
    TRY_CAST("Totale posti letto" AS BIGINT) AS totale_posti_letto
FROM raw_input
WHERE TRY_CAST("Anno" AS INTEGER) IS NOT NULL
  AND TRY_CAST("Totale posti letto" AS BIGINT) IS NOT NULL
