-- MinLavoro flussi — MART: gap di genere su attivazioni/cessazioni.
-- Base: NOTA tabelle 03/07 (genere × tipologia, nazionale).
-- Pivot manuale Maschi/Femmine (niente CTE 'pivot' → keyword DuckDB).

WITH base AS (
    SELECT
        anno,
        tipo_flusso,
        genere,
        SUM(valore) AS n_rapporti
    FROM clean_input
    WHERE tabella_id IN ('nota_03', 'nota_07')
      AND genere IN ('Maschi', 'Femmine')
      AND tipologia_contratto IS NOT NULL
      AND indicatore ILIKE 'Numero di rapporti%'
    GROUP BY 1, 2, 3
),
per_genere AS (
    SELECT
        anno,
        tipo_flusso,
        MAX(CASE WHEN genere = 'Maschi' THEN n_rapporti END) AS n_maschi,
        MAX(CASE WHEN genere = 'Femmine' THEN n_rapporti END) AS n_femmine
    FROM base
    GROUP BY 1, 2
)
SELECT
    anno,
    tipo_flusso,
    n_maschi,
    n_femmine,
    n_maschi - n_femmine AS delta_assoluto,
    ROUND(100.0 * (n_maschi - n_femmine) / NULLIF(n_maschi + n_femmine, 0), 2) AS gap_pct
FROM per_genere
WHERE n_maschi IS NOT NULL
  AND n_femmine IS NOT NULL
