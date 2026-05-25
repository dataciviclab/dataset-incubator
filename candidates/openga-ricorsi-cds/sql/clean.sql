-- Clean: Ricorsi Pendenti Consiglio di Stato (OpenGA)
-- DuckDB auto-detect con header: true — le colonne arrivano gia' tipizzate

SELECT
    {year}::INTEGER AS anno,
    "ANNO_MESE_RIFERIMENTO"::BIGINT AS anno_mese_riferimento,
    ("ANNO_MESE_RIFERIMENTO" % 100)::INTEGER AS mese,
    "CODICE_SEDE"::BIGINT AS codice_sede,
    "NOME_SEDE"::VARCHAR AS nome_sede,
    "NUMERO_RICORSI_PENDENTI"::BIGINT AS numero_ricorsi_pendenti
FROM raw_input
