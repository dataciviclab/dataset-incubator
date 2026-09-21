-- Clean: tipizzazione + normalizzazione delle comunicazioni di procedura inPA
-- Input: raw_input (CSV da scripts/harvest_comunicazioni.py)
-- Output: parquet normalizzato, una riga = una comunicazione di procedura

SELECT
    normalize_string(id)                                                    AS id,
    normalize_string(concorso_id)                                           AS concorso_id,
    normalize_string(concorso_title)                                        AS concorso_title,
    normalize_string(subject)                                               AS subject,
    normalize_string(body)                                                  AS body,
    normalize_string(categoria)                                             AS categoria,
    TRY_CAST(data_pubblicazione AS DATE)                                    AS data_pubblicazione,
    normalize_string(ente)                                                  AS ente
FROM raw_input
