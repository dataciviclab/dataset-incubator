-- mart_sintesi_nazionale — IVA: sintesi nazionale per anno
--
-- 1 riga = 1 anno: totali nazionali di contribuenti, volume d'affari,
-- VA fiscale, imposta dovuta/credito, frequenze (quante partite IVA
-- dichiarano ciascuna voce), più delta % vs anno precedente.
-- Serve per: volume +43% (D1), contribuenti -22% (D2), crollo 2020 e
-- rimbalzo (D5), imposta da 114 a 156 MLD (D6), picco 2022 (D10).
--
-- PK: (anno)

WITH all_clean AS (
    SELECT anno, contribuenti,
           volume_frequenza, volume_affari_eur,
           va_frequenza, va_fiscale_eur,
           imposta_dovuta_frequenza, imposta_dovuta_eur,
           imposta_credito_frequenza, imposta_credito_eur
    FROM clean_input
    WHERE anno IS NOT NULL
),
per_anno AS (
    SELECT
        anno,
        SUM(contribuenti) AS contribuenti,
        SUM(volume_frequenza) AS volume_frequenza,
        SUM(volume_affari_eur) AS volume_affari_eur,
        SUM(va_frequenza) AS va_frequenza,
        SUM(va_fiscale_eur) AS va_fiscale_eur,
        SUM(imposta_dovuta_frequenza) AS imposta_dovuta_frequenza,
        SUM(imposta_dovuta_eur) AS imposta_dovuta_eur,
        SUM(imposta_credito_frequenza) AS imposta_credito_frequenza,
        SUM(imposta_credito_eur) AS imposta_credito_eur
    FROM all_clean
    GROUP BY anno
),
con_lag AS (
    SELECT
        anno,
        contribuenti,
        volume_frequenza,
        volume_affari_eur,
        va_frequenza,
        va_fiscale_eur,
        imposta_dovuta_frequenza,
        imposta_dovuta_eur,
        imposta_credito_frequenza,
        imposta_credito_eur,
        LAG(volume_affari_eur) OVER (ORDER BY anno) AS volume_anno_precedente
    FROM per_anno
)
SELECT
    anno,
    contribuenti,
    volume_frequenza,
    ROUND(volume_affari_eur, 0) AS volume_affari_eur,
    va_frequenza,
    ROUND(va_fiscale_eur, 0) AS va_fiscale_eur,
    imposta_dovuta_frequenza,
    ROUND(imposta_dovuta_eur, 0) AS imposta_dovuta_eur,
    imposta_credito_frequenza,
    ROUND(imposta_credito_eur, 0) AS imposta_credito_eur,
    ROUND(va_fiscale_eur / NULLIF(va_frequenza, 0), 0) AS va_per_dichiarante_eur,
    ROUND(100.0 * imposta_credito_frequenza / NULLIF(va_frequenza, 0), 1) AS quota_contribuenti_credito_pct,
    ROUND(100.0 * (volume_affari_eur - volume_anno_precedente) / NULLIF(volume_anno_precedente, 0), 1) AS delta_volume_pct
FROM con_lag
ORDER BY anno
