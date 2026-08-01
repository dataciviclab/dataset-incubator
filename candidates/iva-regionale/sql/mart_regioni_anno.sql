-- mart_regioni_anno — IVA per regione × anno con benchmark nazionale
--
-- 1 riga = 1 regione × anno. Legge TUTTI gli anni dal clean (glob multi-anno).
-- Aggiunge quota % sul volume nazionale, rank e metriche pro-capite.
-- NOTA: i denominatori pro-capite usano la FREQUENZA della voce (numero di
-- partite IVA che dichiarano quella voce), non i contribuenti totali —
-- altrimenti il valore è distorto (es. solo chi ha credito conta in
-- imposta_credito_frequenza).
-- Serve per: volume per regione (D1), Lombardia 31% (D3), produttività VA/
-- contribuente (D4), divario Nord-Sud (D8), Bolzano vs Trento (D9).
--
-- PK: (anno, regione)

WITH all_clean AS (
    SELECT anno, regione, cod_regione, contribuenti,
           volume_frequenza, volume_affari_eur,
           acquisti_frequenza, acquisti_eur,
           va_frequenza, va_fiscale_eur,
           imposta_dovuta_frequenza, imposta_dovuta_eur,
           imposta_credito_frequenza, imposta_credito_eur
    FROM read_parquet(
        '{root}/data/clean/{dataset}/*/{dataset}_*_clean.parquet',
        union_by_name=true
    )
    WHERE anno IS NOT NULL AND regione IS NOT NULL
),
nazionali AS (
    SELECT
        anno,
        SUM(volume_affari_eur) AS volume_nazionale,
        SUM(contribuenti) AS contribuenti_nazionali
    FROM all_clean
    GROUP BY anno
)
SELECT
    c.anno,
    c.regione,
    c.cod_regione,
    c.contribuenti,
    c.volume_frequenza,
    ROUND(c.volume_affari_eur, 0) AS volume_affari_eur,
    c.acquisti_frequenza,
    ROUND(c.acquisti_eur, 0) AS acquisti_eur,
    c.va_frequenza,
    ROUND(c.va_fiscale_eur, 0) AS va_fiscale_eur,
    c.imposta_dovuta_frequenza,
    ROUND(c.imposta_dovuta_eur, 0) AS imposta_dovuta_eur,
    c.imposta_credito_frequenza,
    ROUND(c.imposta_credito_eur, 0) AS imposta_credito_eur,
    ROUND(c.va_fiscale_eur / NULLIF(c.va_frequenza, 0), 0) AS va_per_dichiarante_eur,
    ROUND(c.volume_affari_eur / NULLIF(c.volume_frequenza, 0), 0) AS volume_per_dichiarante_eur,
    ROUND(100.0 * c.imposta_credito_frequenza / NULLIF(c.va_frequenza, 0), 1) AS quota_contribuenti_credito_pct,
    ROUND(100.0 * c.volume_affari_eur / NULLIF(n.volume_nazionale, 0), 1) AS quota_volume_pct,
    ROW_NUMBER() OVER (PARTITION BY c.anno ORDER BY c.volume_affari_eur DESC) AS rank_volume
FROM all_clean c
JOIN nazionali n USING (anno)
ORDER BY c.anno, rank_volume
