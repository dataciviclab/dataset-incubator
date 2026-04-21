select
    cast(ANNO_SOLARE as integer) as anno,
    cast(COD_Ateneo as integer) as cod_ateneo,
    NOME_ATENEO,
    CODICE_GETTITO,
    DESCRIZIONE_GETTITO,
    -- CONTO_ECONOMICO uses comma as decimal separator
    cast(replace(CONTO_ECONOMICO, ',', '.') as double) as euro_contributo
from raw_input