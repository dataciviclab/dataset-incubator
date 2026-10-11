-- clean.sql: tasso occupazione province (150_915)
-- Canale dbnomics · macros toolkit (normalize_string / cast_int / cast_double)

SELECT
    normalize_string(REF_AREA) AS ref_area,
    normalize_string(REF_AREA) AS territorio,
    cast_int(TIME_PERIOD) AS anno,
    normalize_string(DATA_TYPE) AS indicatore,
    normalize_string(SEX) AS sesso_codice,
    case normalize_string(SEX)
        when '1' then 'maschi'
        when '2' then 'femmine'
        when '9' then 'totale'
        else normalize_string(SEX)
    end AS sesso,
    normalize_string(AGE) AS eta_codice,
    normalize_string(AGE) AS eta,
    cast_double(OBS_VALUE) AS valore
FROM raw_input
WHERE
    normalize_string(FREQ) = 'A'
    AND length(normalize_string(REF_AREA)) = 5
    AND normalize_string(CITIZENSHIP) = 'TOTAL'
    AND normalize_string(EDU_LEV_HIGHEST) = '99'
    AND normalize_string(AGE) IN ('Y15-64', 'Y15-24', 'Y25-34', 'Y35-44', 'Y45-54', 'Y55-64')
    AND normalize_string(DATA_TYPE) IN ('EMP_R', 'UNEM_R')
    AND anno IS NOT NULL
    AND valore IS NOT NULL
