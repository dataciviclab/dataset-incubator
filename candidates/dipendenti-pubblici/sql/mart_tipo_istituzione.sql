-- Dipendenti Pubblici: Organico per tipo istituzione e anno
-- Trend dimensionale per macrotipo (Comuni, ASL, Scuole, Universita', ecc.)
WITH base AS (
    SELECT
        anno,
        tipo_istituzione,
        (donne_tempo_pieno + donne_part_time_inf_50 + donne_part_time_sup_50
         + uomini_tempo_pieno + uomini_part_time_inf_50 + uomini_part_time_sup_50) AS organico,
        donne_assunte + uomini_assunti AS assunti,
        donne_cessate + uomini_cessati AS cessati
    FROM clean_input
)
SELECT
    anno,
    tipo_istituzione,
    ROUND(SUM(organico), 0) AS organico_totale,
    ROUND(AVG(organico), 0) AS organico_medio_per_ente,
    COUNT(*) AS enti,
    ROUND(SUM(assunti), 0) AS assunti_totali,
    ROUND(SUM(cessati), 0) AS cessati_totali,
    ROUND(SUM(assunti) - SUM(cessati), 0) AS saldo_netto,
    -- Variazione % organico rispetto anno precedente
    ROUND((SUM(organico) - LAG(SUM(organico)) OVER (PARTITION BY tipo_istituzione ORDER BY anno))
        * 100.0 / NULLIF(LAG(SUM(organico)) OVER (PARTITION BY tipo_istituzione ORDER BY anno), 0), 2)
        AS var_organico_pct
FROM base
WHERE tipo_istituzione IS NOT NULL
GROUP BY anno, tipo_istituzione
ORDER BY anno DESC, organico_totale DESC
