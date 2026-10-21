-- mart: serie nazionale Italia (riga Eurostat TOTAL)
-- Reiterate: pubblicate solo dal 2021, prima derivate da (totale - prima istanza).
WITH italia AS (
    SELECT
        anno,
        CAST(sum(CASE WHEN misura = 'domande' AND dettaglio_codice = 'TOTAL' THEN valore END) AS BIGINT) AS domande,
        CAST(sum(CASE WHEN misura = 'domande' AND dettaglio_codice = 'FRST' THEN valore END) AS BIGINT) AS domande_prima_istanza,
        CAST(sum(CASE WHEN misura = 'domande' AND dettaglio_codice = 'SSEQ' THEN valore END) AS BIGINT) AS reiterate_pubblicate,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'TOTAL' THEN valore END) AS BIGINT) AS decisioni,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'POS' THEN valore END) AS BIGINT) AS accolte,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'POS_RFG' THEN valore END) AS BIGINT) AS rifugiati,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'POS_SPROT' THEN valore END) AS BIGINT) AS protezione_sussidiaria,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'POS_HUM' THEN valore END) AS BIGINT) AS protezione_umanitaria,
        CAST(sum(CASE WHEN misura = 'decisioni' AND dettaglio_codice = 'NEG' THEN valore END) AS BIGINT) AS dinieghi
    FROM clean_input
    WHERE cittadinanza_codice = 'TOTAL'
    GROUP BY anno
),
calcolate AS (
    SELECT
        *,
        CASE
            WHEN reiterate_pubblicate IS NOT NULL THEN reiterate_pubblicate
            WHEN domande IS NOT NULL AND domande_prima_istanza IS NOT NULL
                THEN greatest(domande - domande_prima_istanza, 0)
        END AS domande_reiterate,
        CASE
            WHEN reiterate_pubblicate IS NOT NULL THEN FALSE
            WHEN domande IS NOT NULL AND domande_prima_istanza IS NOT NULL THEN TRUE
        END AS reiterate_derivate
    FROM italia
)
SELECT
    anno,
    domande,
    domande_prima_istanza,
    domande_reiterate,
    reiterate_derivate,
    decisioni,
    accolte,
    rifugiati,
    protezione_sussidiaria,
    protezione_umanitaria,
    dinieghi,
    CASE WHEN decisioni > 0 THEN round(accolte * 1.0 / decisioni, 4) END AS tasso_riconoscimento,
    CASE WHEN decisioni > 0 THEN round(dinieghi * 1.0 / decisioni, 4) END AS tasso_diniego,
    CASE WHEN domande > 0 THEN round(domande_reiterate * 1.0 / domande, 4) END AS quota_reiterate
FROM calcolate
WHERE domande IS NOT NULL
   OR decisioni IS NOT NULL
ORDER BY anno
