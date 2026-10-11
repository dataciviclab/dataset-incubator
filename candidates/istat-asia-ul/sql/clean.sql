-- Clean ASIA UL: unità locali + addetti per comune × ATECO × anno
-- Canale: script preprocess (CSV: data_type, ref_area, anno, ateco_sezione, valore)
-- Macros toolkit · join istat_elenco_comuni (GCS)

WITH raw AS (
    SELECT
        normalize_string(data_type)              AS data_type,
        normalize_string(ref_area)               AS ref_area,
        cast_int(anno)                           AS anno,
        normalize_string(ateco_sezione)          AS ateco_sezione,
        cast_double(valore)                      AS valore
    FROM raw_input
    WHERE
        length(normalize_string(ref_area)) = 6
        AND cast_bigint(normalize_string(ref_area)) IS NOT NULL
        AND anno IS NOT NULL
        AND anno BETWEEN 2018 AND 2020
        AND normalize_string(data_type) IN ('LU', 'LUEMPDAA')
        AND cast_double(valore) >= 0
        AND cast_double(valore) IS NOT NULL
),

comuni AS (
    SELECT * FROM read_parquet(
        'https://storage.googleapis.com/dataciviclab-clean/istat_elenco_comuni/2026/istat_elenco_comuni_2026_clean.parquet'
    )
)

SELECT
    r.data_type,
    r.ref_area AS codice_comune,
    r.anno,
    r.ateco_sezione,
    r.valore,
    c.denominazione,
    c.regione,
    c.sigla_provincia
FROM raw r
LEFT JOIN comuni c ON r.ref_area = c.codice_istat
