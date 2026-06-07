select
    cast("ANNO_SOLARE" as integer) as anno,
    cast("COD_Ateneo" as integer) as cod_ateneo,
    "NOME_ATENEO" as nome_ateneo,
    "CODICE_GETTITO" as codice_gettito,
    "DESCRIZIONE_GETTITO" as descrizione_gettito,
    -- CONTO_ECONOMICO: portale MUR alterna formato double (2018-2022,2024)
    -- e stringa con virgola decimale (2017,2023). cast via varchar è robusto per entrambi.
    cast(replace(cast("CONTO_ECONOMICO" as varchar), ',', '.') as double) as euro_contributo
from raw_input
