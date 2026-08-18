-- Clean: tipizzazione + normalizzazione del CSV flat prodotto da harvest_inpa.py
-- Input: raw_input (CSV da scripts/harvest_inpa.py, unione OPEN+CLOSED con union_by_name)
-- Output: parquet normalizzato, una riga = un bando inPA
-- Dedup: 31 id compaiono sia in OPEN che in CLOSED (overlap API) → priorità a OPEN (ha il dettaglio)

WITH typed AS (
    SELECT
        normalize_string(id)                                                    AS id,
        normalize_string(codice)                                                AS codice,
        normalize_string(titolo)                                                AS titolo,
        normalize_string(figura_ricercata)                                      AS figura_ricercata,
        TRY_CAST(normalize_string(descrizione) AS VARCHAR)                      AS descrizione,
        CASE WHEN EXTRACT(YEAR FROM TRY_CAST(data_pubblicazione AS DATE)) >= 2000
             THEN TRY_CAST(data_pubblicazione AS DATE) END                      AS data_pubblicazione,
        CASE WHEN EXTRACT(YEAR FROM TRY_CAST(data_scadenza AS DATE)) >= 2000
             THEN TRY_CAST(data_scadenza AS DATE) END                           AS data_scadenza,
        CASE WHEN EXTRACT(YEAR FROM TRY_CAST(data_visibilita AS DATE)) >= 2000
             THEN TRY_CAST(data_visibilita AS DATE) END                         AS data_visibilita,
        normalize_string(tipo_procedura)                                        AS tipo_procedura,
        -- Sentinella: valori "tutti 9" (9999/99999/999999) usati come N/D per
        -- gli "Elenchi di Idonei" (scorrimento, posti non definiti). I valori
        -- alti reali (es. 30.000 supplenze scolastiche) restano validi.
        CASE WHEN cast_int(num_posti) IS NOT NULL
                  AND NOT (regexp_matches(cast_int(num_posti)::VARCHAR, '^9+$') AND cast_int(num_posti) > 99)
             THEN cast_int(num_posti) END                                    AS num_posti,
        normalize_string(status)                                                AS status,
        normalize_string(status_label)                                          AS status_label,
        normalize_string(categoria)                                             AS categoria,
        normalize_string(settore)                                               AS settore,
        normalize_string(regione)                                               AS regione,
        normalize_string(provincia)                                             AS provincia,
        normalize_string(ente)                                                  AS ente,
        normalize_string(enti_riferimento)                                      AS enti_riferimento,
        normalize_string(categorie)                                             AS categorie,
        normalize_string(settori)                                               AS settori,
        normalize_string(sedi)                                                  AS sedi,
        normalize_string(company_district_code)                                 AS company_district_code,
        normalize_string(link_sito_pa)                                          AS link_sito_pa,
        decode_flag(richiede_pagamento, 'True')                                 AS richiede_pagamento,
        decode_flag(pec_obbligatoria, 'True')                                   AS pec_obbligatoria,
        decode_flag(is_remote, 'SI')                                            AS is_remote,
        cast_double(salary_min)                                                 AS salary_min,
        cast_double(salary_max)                                                 AS salary_max,
        normalize_string(link_gazzetta_ufficiale)                               AS link_gazzetta_ufficiale,
        cast_int(n_allegati)                                                    AS n_allegati,
        ROW_NUMBER() OVER (PARTITION BY normalize_string(id)
                           ORDER BY CASE WHEN normalize_string(status) = 'OPEN' THEN 0 ELSE 1 END) AS rn
    FROM raw_input
)
SELECT
    id, codice, titolo, figura_ricercata, descrizione,
    data_pubblicazione, data_scadenza, data_visibilita, tipo_procedura, num_posti,
    status, status_label, categoria, settore, regione, provincia, ente,
    enti_riferimento, categorie, settori, sedi,
    company_district_code, link_sito_pa, richiede_pagamento, pec_obbligatoria,
    is_remote, salary_min, salary_max, link_gazzetta_ufficiale, n_allegati
FROM typed
WHERE rn = 1
