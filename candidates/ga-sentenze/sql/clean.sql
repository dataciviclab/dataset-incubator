SELECT
    cast_bigint("ANNO_PUBBLICAZIONE") AS anno,
    cast_bigint("CODICE_SEDE") AS codice_sede,
    normalize_string("NOME_SEDE") AS nome_sede,
    normalize_string("CODICE_SEZIONE") AS codice_sezione,
    normalize_string("NOME_SEZIONE") AS nome_sezione,
    cast_bigint("NUMERO_PROVVEDIMENTO") AS numero_provvedimento,
    cast_bigint("NUMERO_RICORSO") AS numero_ricorso,
    TRY_CAST("DATA_PUBBLICAZIONE" AS DATE) AS data_pubblicazione,
    cast_bigint("MESE_PUBBLICAZIONE") AS mese_pubblicazione,
    normalize_string("ESITO_PROVVEDIMENTO") AS esito_provvedimento,
    normalize_string("FLG_DEFINISCE") AS flg_definisce,
    TRY_CAST("DATA_DEPOSITO_RICORSO" AS DATE) AS data_deposito_ricorso,
    normalize_string("OGGETTO_RICORSO") AS oggetto_ricorso,
    normalize_string("TIPO_RICORSO") AS tipo_ricorso,
    normalize_string("TIPO_UDIENZA") AS tipo_udienza,
    cast_bigint("NUM_MEMBRI_COLLEGIO") AS num_membri_collegio,
    normalize_string("TIPO_PROVVEDIMENTO") AS tipo_provvedimento
FROM raw_input
