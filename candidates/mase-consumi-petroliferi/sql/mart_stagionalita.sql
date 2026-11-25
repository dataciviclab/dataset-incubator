-- Stagionalità dei consumi petroliferi: quanto pesa ogni mese sul totale annuo,
-- mediato sugli anni disponibili. Una riga per prodotto × mese.
--
-- `indice` è la quota del mese rapportata a un anno piatto (100/12 = 8,33):
--   > 1 mese sopra la media · < 1 sotto. Serve per leggere il picco estivo
--   della benzina e quello invernale del GPL.
-- Esclude la riga di sintesi `totale prodotti principali`.
--
-- PK: (prodotto, mese)

WITH mensile AS (
    SELECT anno, mese, prodotto, consumo_kt
    FROM clean_input
    WHERE prodotto <> 'totale prodotti principali'
),
totale_anno AS (
    SELECT anno, prodotto, SUM(consumo_kt) AS consumo_anno
    FROM mensile
    GROUP BY anno, prodotto
),
quote AS (
    SELECT
        m.prodotto,
        m.mese,
        100.0 * m.consumo_kt / NULLIF(t.consumo_anno, 0) AS quota_mese_pct
    FROM mensile m
    JOIN totale_anno t USING (anno, prodotto)
)
SELECT
    prodotto,
    mese,
    ROUND(AVG(quota_mese_pct), 2) AS quota_mese_media_pct,
    ROUND(AVG(quota_mese_pct) / (100.0 / 12.0), 3) AS indice,
    COUNT(*) AS n_anni
FROM quote
GROUP BY prodotto, mese
