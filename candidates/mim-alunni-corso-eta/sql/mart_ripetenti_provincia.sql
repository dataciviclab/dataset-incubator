-- mart_ripetenti_provincia — Alunni in età non allineata al corso per provincia
--
-- 1 riga = 1 provincia × ordine (ultimo anno): alunni in età "non regolare"
-- rispetto al corso (ripetenti + anticipatari + irregolari).
-- Logica: per ogni ordine l'età attesa = corso + offset
--   primaria: corso+5 · secondaria I: corso+10 · secondaria II: corso+13
-- Gli alunni con età diversa dall'attesa sono "non allineati".
-- Serve per: province con più ripetenti (mappa #163).
--
-- PK: (provincia, ordine_scuola)

WITH base AS (
    SELECT
        anno_scolastico,
        provincia,
        ordine_scuola,
        anno_corso,
        fascia_eta,
        alunni,
        CASE ordine_scuola
            WHEN 'SCUOLA PRIMARIA' THEN CAST(anno_corso AS INTEGER) + 5
            WHEN 'SCUOLA SECONDARIA I GRADO' THEN CAST(anno_corso AS INTEGER) + 10
            WHEN 'SCUOLA SECONDARIA II GRADO' THEN CAST(anno_corso AS INTEGER) + 13
        END AS eta_attesa,
        TRY_CAST(REGEXP_EXTRACT(fascia_eta, '(\d+)') AS INTEGER) AS eta_effettiva
    FROM clean_input
    WHERE alunni IS NOT NULL AND provincia IS NOT NULL
),
per_anno AS (
    SELECT
        anno_scolastico,
        provincia,
        ordine_scuola,
        SUM(alunni) AS alunni_tot,
        SUM(CASE WHEN eta_effettiva IS NOT NULL AND eta_effettiva != eta_attesa THEN alunni ELSE 0 END) AS alunni_non_allineati
    FROM base
    GROUP BY anno_scolastico, provincia, ordine_scuola
),
ultimo AS (
    SELECT anno_scolastico, provincia, ordine_scuola, alunni_tot, alunni_non_allineati,
           ROW_NUMBER() OVER (PARTITION BY provincia, ordine_scuola ORDER BY anno_scolastico DESC) AS rn
    FROM per_anno
)
SELECT
    anno_scolastico,
    provincia,
    ordine_scuola,
    alunni_tot,
    alunni_non_allineati,
    ROUND(100.0 * alunni_non_allineati / NULLIF(alunni_tot, 0), 2) AS quota_non_allineati_pct
FROM ultimo
WHERE rn = 1
ORDER BY quota_non_allineati_pct DESC
