SELECT
    TRY_CAST("ANNO_PUBBLICAZIONE" AS BIGINT) AS anno,
    TRY_CAST("CODICE_SEDE" AS BIGINT) AS codice_sede,
    TRY_CAST("NOME_SEDE" AS VARCHAR) AS nome_sede,
    TRY_CAST("CODICE_SEZIONE" AS VARCHAR) AS codice_sezione,
    TRY_CAST("NOME_SEZIONE" AS VARCHAR) AS nome_sezione,
    TRY_CAST("NUMERO_PROVVEDIMENTO" AS BIGINT) AS numero_provvedimento,
    TRY_CAST("NUMERO_RICORSO" AS BIGINT) AS numero_ricorso,
    TRY_CAST("DATA_PUBBLICAZIONE" AS DATE) AS data_pubblicazione,
    TRY_CAST("MESE_PUBBLICAZIONE" AS BIGINT) AS mese_pubblicazione,
    TRY_CAST("ESITO_PROVVEDIMENTO" AS VARCHAR) AS esito_provvedimento,
    TRY_CAST("FLG_DEFINISCE" AS VARCHAR) AS flg_definisce,
    TRY_CAST("DATA_DEPOSITO_RICORSO" AS DATE) AS data_deposito_ricorso,
    TRY_CAST("OGGETTO_RICORSO" AS VARCHAR) AS oggetto_ricorso,
    TRY_CAST("TIPO_RICORSO" AS VARCHAR) AS tipo_ricorso,
    TRY_CAST("TIPO_UDIENZA" AS VARCHAR) AS tipo_udienza,
    TRY_CAST("NUM_MEMBRI_COLLEGIO" AS BIGINT) AS num_membri_collegio,
    TRY_CAST("TIPO_PROVVEDIMENTO" AS VARCHAR) AS tipo_provvedimento
FROM read_csv_auto(
    '{root}/data/raw/ga_sentenze/{year}/*.csv',
    union_by_name=true,
    header=true
)
