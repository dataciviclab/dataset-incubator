-- mart_trend_ordine — Alunni per ordine scolastico × anno
--
-- 1 riga = 1 anno_scolastico × ordine: totale alunni, delta vs anno
-- precedente e variazione %. Serie temporale completa.
-- Serve per: quanti alunni per ordine (mappa #162), evoluzione 2016-2025.
--
-- PK: (anno_scolastico, ordine_scuola)

WITH base AS (
    SELECT anno_scolastico, ordine_scuola, SUM(alunni) AS alunni
    FROM clean_input
    WHERE alunni IS NOT NULL
    GROUP BY anno_scolastico, ordine_scuola
),
con_lag AS (
    SELECT
        anno_scolastico,
        ordine_scuola,
        alunni,
        LAG(alunni) OVER (PARTITION BY ordine_scuola ORDER BY anno_scolastico) AS alunni_anno_precedente
    FROM base
)
SELECT
    anno_scolastico,
    ordine_scuola,
    alunni,
    alunni_anno_precedente,
    alunni - alunni_anno_precedente AS delta_alunni,
    ROUND(100.0 * (alunni - alunni_anno_precedente) / NULLIF(alunni_anno_precedente, 0), 1) AS variazione_pct
FROM con_lag
ORDER BY ordine_scuola, anno_scolastico
