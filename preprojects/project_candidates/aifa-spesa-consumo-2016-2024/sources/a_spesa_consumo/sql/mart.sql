-- mart.sql - aifa_spesa_consumo - mart_mensile_regione_atc4
-- Primo taglio analitico:
-- - usa solo flusso convenzionata (gia filtrato nel clean)
-- - aggrega a livello anno x mese x regione x atc4
-- - calcola quota percentuale della spesa atc4 sul totale regionale del mese

WITH base AS (
    SELECT
        anno,
        mese,
        codreg,
        regione,
        atc1,
        descrizione_atc1,
        atc2,
        descrizione_atc2,
        atc3,
        descrizione_atc3,
        atc4,
        descrizione_atc4,
        SUM(numero_confezioni_convenzionata)  AS num_confezioni,
        SUM(spesa_convenzionata)              AS spesa_convenzionata
    FROM clean_input
    GROUP BY
        anno, mese, codreg, regione,
        atc1, descrizione_atc1, atc2, descrizione_atc2, atc3, descrizione_atc3, atc4, descrizione_atc4
),
totali_regione_mese AS (
    SELECT
        anno,
        mese,
        codreg,
        SUM(spesa_convenzionata) AS spesa_totale_regione_mese
    FROM base
    GROUP BY anno, mese, codreg
)
SELECT
    b.anno,
    b.mese,
    b.codreg,
    b.regione,
    b.atc1,
    b.descrizione_atc1,
    b.atc2,
    b.descrizione_atc2,
    b.atc3,
    b.descrizione_atc3,
    b.atc4,
    b.descrizione_atc4,
    ROUND(b.num_confezioni, 0)                                                           AS num_confezioni,
    ROUND(b.spesa_convenzionata, 2)                                                      AS spesa_convenzionata,
    ROUND(t.spesa_totale_regione_mese, 2)                                                AS spesa_totale_regione_mese,
    ROUND(b.spesa_convenzionata / NULLIF(t.spesa_totale_regione_mese, 0) * 100, 4)      AS quota_spesa_regione_pct
FROM base b
JOIN totali_regione_mese t
  ON b.anno   = t.anno
 AND b.mese   = t.mese
 AND b.codreg = t.codreg
ORDER BY b.anno, b.mese, b.regione, b.spesa_convenzionata DESC
