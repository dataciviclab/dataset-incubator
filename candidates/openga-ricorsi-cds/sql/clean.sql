-- Clean: Ricorsi Pendenti Consiglio di Stato (OpenGA)
-- DuckDB auto-detect con header: true — le colonne arrivano gia' tipizzate

SELECT
    {year}::INTEGER AS anno,
    cast_bigint("ANNO_MESE_RIFERIMENTO") AS anno_mese_riferimento,
    (cast_bigint("ANNO_MESE_RIFERIMENTO") % 100)::INTEGER AS mese,
    cast_bigint("CODICE_SEDE") AS codice_sede,
    normalize_string("NOME_SEDE") AS nome_sede,
    cast_bigint("NUMERO_RICORSI_PENDENTI") AS numero_ricorsi_pendenti
FROM raw_input
