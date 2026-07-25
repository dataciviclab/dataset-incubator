-- IRPEF: Distribuzione contribuenti per fascia di reddito complessivo
-- Quota di contribuenti in ogni fascia (0-10k, 10-15k, 15-26k, 26-55k,
-- 55-75k, 75-120k, oltre 120k) per provincia/regione.
SELECT
    anno_di_imposta AS anno,
    regione,
    sigla_provincia AS provincia,
    COUNT(*) AS comuni,
    SUM(numero_contribuenti) AS contribuenti_totale,
    -- Contribuenti per fascia
    ROUND(SUM(reddito_complessivo_minore_o_uguale_a_zero_euro_freq), 0) AS fascia_zero,
    ROUND(SUM(reddito_complessivo_da_0_a_10000_euro_freq), 0) AS fascia_0_10k,
    ROUND(SUM(reddito_complessivo_da_10000_a_15000_euro_freq), 0) AS fascia_10_15k,
    ROUND(SUM(reddito_complessivo_da_15000_a_26000_euro_freq), 0) AS fascia_15_26k,
    ROUND(SUM(reddito_complessivo_da_26000_a_55000_euro_freq), 0) AS fascia_26_55k,
    ROUND(SUM(reddito_complessivo_da_55000_a_75000_euro_freq), 0) AS fascia_55_75k,
    ROUND(SUM(reddito_complessivo_da_75000_a_120000_euro_freq), 0) AS fascia_75_120k,
    ROUND(SUM(reddito_complessivo_oltre_120000_euro_freq), 0) AS fascia_oltre_120k,
    -- Quote percentuali
    ROUND(SUM(reddito_complessivo_da_0_a_10000_euro_freq) * 100.0 / NULLIF(SUM(numero_contribuenti), 0), 2) AS quota_0_10k_pct,
    ROUND((SUM(reddito_complessivo_da_55000_a_75000_euro_freq)
        + SUM(reddito_complessivo_da_75000_a_120000_euro_freq)
        + SUM(reddito_complessivo_oltre_120000_euro_freq)) * 100.0 / NULLIF(SUM(numero_contribuenti), 0), 2) AS quota_oltre_55k_pct
FROM clean_input
WHERE regione IS NOT NULL
GROUP BY anno, regione, provincia
ORDER BY anno DESC, contribuenti_totale DESC
