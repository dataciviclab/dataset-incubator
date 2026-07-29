-- Clean: elezioni referendum — risultati per comune/quesito (1995-2022)
-- Usa macro standard del toolkit: cast_bigint, normalize_string

SELECT
    CAST(data_elezione AS DATE) AS data_elezione,
    normalize_string(regione) AS regione,
    normalize_string(provincia) AS provincia,
    normalize_string(comune) AS comune,
    cast_bigint(elettori_uomini) AS elettori_uomini,
    cast_bigint(elettori) AS elettori,
    cast_bigint(votanti_uomini) AS votanti_uomini,
    cast_bigint(votanti) AS votanti,
    cast_bigint(voti_si) AS voti_si,
    cast_bigint(voti_no) AS voti_no,
    cast_bigint(schede_nulle) AS schede_nulle,
    cast_bigint(schede_bianche) AS schede_bianche,
    cast_bigint(schede_contestate) AS schede_contestate,
    cast_bigint(num_quesito) AS num_quesito
FROM raw_input
