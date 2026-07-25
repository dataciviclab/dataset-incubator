-- Dipendenti Pubblici: Incidenza part-time per genere, comparto e anno
-- Il part-time e' prevalentemente femminile? sta cambiando?
WITH base AS (
    SELECT
        anno,
        comparto,
        -- part time: inf_50 + sup_50 per genere
        (donne_part_time_inf_50 + donne_part_time_sup_50) AS donne_part_time,
        (uomini_part_time_inf_50 + uomini_part_time_sup_50) AS uomini_part_time,
        (donne_tempo_pieno + donne_part_time_inf_50 + donne_part_time_sup_50) AS donne_totali,
        (uomini_tempo_pieno + uomini_part_time_inf_50 + uomini_part_time_sup_50) AS uomini_totali
    FROM clean_input
)
SELECT
    anno,
    comparto,
    ROUND(SUM(donne_totali + uomini_totali), 0) AS dipendenti_totali,
    -- Part-time femminile
    ROUND(SUM(donne_part_time), 0) AS donne_part_time,
    ROUND(SUM(donne_part_time) * 100.0 / NULLIF(SUM(donne_totali), 0), 2) AS donne_pt_pct,
    -- Part-time maschile
    ROUND(SUM(uomini_part_time), 0) AS uomini_part_time,
    ROUND(SUM(uomini_part_time) * 100.0 / NULLIF(SUM(uomini_totali), 0), 2) AS uomini_pt_pct,
    -- Totale part-time
    ROUND(SUM(donne_part_time + uomini_part_time), 0) AS pt_totale,
    ROUND(SUM(donne_part_time + uomini_part_time) * 100.0 / NULLIF(SUM(donne_totali + uomini_totali), 0), 2) AS pt_su_totale_pct,
    -- Quota donne tra i part-time
    ROUND(SUM(donne_part_time) * 100.0 / NULLIF(SUM(donne_part_time + uomini_part_time), 0), 2) AS donne_su_pt_pct
FROM base
GROUP BY anno, comparto
ORDER BY anno DESC, dipendenti_totali DESC
