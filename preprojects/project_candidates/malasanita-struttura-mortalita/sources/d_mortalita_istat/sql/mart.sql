-- mart.sql - malasanita_d_mortalita_istat - mart_regioni
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Scelta metodologica v1:
-- - usiamo solo il livello totale su sesso, classe eta e titolo di studio
-- - usiamo la causa "Totale" (cod_causa = 25)
-- - evitiamo quindi il sovraconto che si avrebbe sommando tutte le righe clean
--
-- Questa tabella e` un output regionale pulito per il compose successivo.

WITH base AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        decessi,
        pop_media,
        tasso_std_10000
    FROM clean_input
    WHERE cod_sesso = 3
      AND cod_classe_eta = 9
      AND cod_titolo_studio = 9
      AND cod_causa = 25
)
SELECT
    anno,
    cod_territorio,
    territorio,
    decessi AS decessi_totali,
    pop_media AS pop_media_30_plus,
    tasso_std_10000 AS tasso_std_10000_30_plus,
    ROUND(tasso_std_10000 * 10.0, 2) AS tasso_std_100k_30_plus
FROM base
ORDER BY cod_territorio
