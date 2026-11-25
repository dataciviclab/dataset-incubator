-- Share % di VA per branca NACE nella regione
-- Solo sezioni singole A–S (partizione non sovrapposta).
-- Denominatore: _T se presente, altrimenti somma A–S.
-- Anni senza sezioni dettagliate (es. 2023 in edizione 2025M6): nessuna riga share —
-- usare mart_va_branca (codici aggregati) per l'esplorazione.

WITH va AS (
    SELECT
        territorio_codice,
        territorio_nome,
        anno,
        nace_codice,
        valore_mln_eu
    FROM clean_input
    WHERE tipo_dato_codice = 'B1G_B_W2_S1'
      AND valutazione_codice = 'V'
      AND valore_mln_eu IS NOT NULL
),
sezioni AS (
    SELECT *
    FROM va
    WHERE LENGTH(nace_codice) = 1
      AND nace_codice BETWEEN 'A' AND 'S'
),
totale AS (
    SELECT
        territorio_codice,
        anno,
        valore_mln_eu AS va_totale_mln_eu
    FROM va
    WHERE nace_codice = '_T'
),
somma_sezioni AS (
    SELECT
        territorio_codice,
        anno,
        SUM(valore_mln_eu) AS va_totale_mln_eu
    FROM sezioni
    GROUP BY 1, 2
),
denom AS (
    SELECT
        COALESCE(t.territorio_codice, s.territorio_codice) AS territorio_codice,
        COALESCE(t.anno, s.anno) AS anno,
        COALESCE(t.va_totale_mln_eu, s.va_totale_mln_eu) AS va_totale_mln_eu,
        CASE WHEN t.va_totale_mln_eu IS NOT NULL THEN '_T' ELSE 'SUM_A_S' END AS fonte_totale
    FROM totale t
    FULL OUTER JOIN somma_sezioni s
        ON t.territorio_codice = s.territorio_codice AND t.anno = s.anno
)
SELECT
    v.territorio_codice,
    v.territorio_nome,
    v.anno,
    v.nace_codice,
    v.valore_mln_eu AS va_mln_eu,
    d.va_totale_mln_eu,
    d.fonte_totale,
    ROUND(100.0 * v.valore_mln_eu / NULLIF(d.va_totale_mln_eu, 0), 2) AS share_pct
FROM sezioni v
JOIN denom d
    ON v.territorio_codice = d.territorio_codice AND v.anno = d.anno
WHERE d.va_totale_mln_eu > 0
ORDER BY v.territorio_codice, v.anno, v.nace_codice
