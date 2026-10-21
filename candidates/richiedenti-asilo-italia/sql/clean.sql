-- clean.sql: Eurostat domande + decisioni asilo (Italia)
-- Schema raw: misura, anno, cittadinanza_codice, cittadinanza, dettaglio_codice, valore
-- Etichette cittadinanza: codelist Eurostat CITIZEN (inglese, fedelta' alla fonte).
-- aggregato: codice non ISO-3166 alpha-2 (TOTAL, EU*, EXT_EU27_2020, UK_OCT, UNK...),
-- con eccezione per RNC (recognised non-citizens) e STLS (apolidi), che sono
-- categorie di persone e non totali.

SELECT
    cast_int(anno) AS anno,
    normalize_string(cittadinanza_codice) AS cittadinanza_codice,
    normalize_string(cittadinanza) AS cittadinanza,
    normalize_string(misura) AS misura,
    normalize_string(dettaglio_codice) AS dettaglio_codice,
    CASE normalize_string(dettaglio_codice)
        WHEN 'TOTAL' THEN
            CASE normalize_string(misura)
                WHEN 'domande' THEN 'Totale domande'
                ELSE 'Totale decisioni'
            END
        WHEN 'FRST' THEN 'Prima istanza'
        WHEN 'SSEQ' THEN 'Domande reiterate'
        WHEN 'POS' THEN 'Accolte (totale)'
        WHEN 'POS_RFG' THEN 'Status di rifugiato'
        WHEN 'POS_SPROT' THEN 'Protezione sussidiaria'
        WHEN 'POS_HUM' THEN 'Protezione umanitaria'
        WHEN 'NEG' THEN 'Dinieghi'
        ELSE normalize_string(dettaglio_codice)
    END AS dettaglio,
    cast_bigint(valore) AS valore,
    COALESCE(
        NOT regexp_full_match(normalize_string(cittadinanza_codice), '[A-Z]{2}')
            AND normalize_string(cittadinanza_codice) NOT IN ('STLS', 'RNC'),
        TRUE
    ) AS aggregato
FROM raw_input
WHERE cast_int(anno) IS NOT NULL
  AND cast_bigint(valore) IS NOT NULL
