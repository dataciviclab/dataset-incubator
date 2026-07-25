-- Dipendenti Pubblici: Enti con maggior turnover
-- (assunti + cessati) / organico per ente, anno e comparto.
-- Segnali di criticita' o rinnovo generazionale.
WITH base AS (
    SELECT
        anno,
        ente,
        comparto,
        tipo_istituzione,
        (donne_tempo_pieno + donne_part_time_inf_50 + donne_part_time_sup_50
         + uomini_tempo_pieno + uomini_part_time_inf_50 + uomini_part_time_sup_50) AS organico,
        (donne_assunte + uomini_assunti) AS assunti,
        (donne_cessate + uomini_cessati) AS cessati
    FROM clean_input
    WHERE ente IS NOT NULL
)
SELECT
    anno,
    ente,
    comparto,
    tipo_istituzione,
    ROUND(SUM(organico), 0) AS organico_totale,
    ROUND(SUM(assunti), 0) AS assunti_totali,
    ROUND(SUM(cessati), 0) AS cessati_totali,
    ROUND(SUM(assunti) - SUM(cessati), 0) AS saldo_netto,
    ROUND((SUM(assunti) + SUM(cessati)) * 100.0 / NULLIF(SUM(organico), 0), 2) AS tasso_turnover_pct,
    ROUND(SUM(assunti) * 100.0 / NULLIF(SUM(organico), 0), 2) AS tasso_assunzione_pct,
    ROUND(SUM(cessati) * 100.0 / NULLIF(SUM(organico), 0), 2) AS tasso_uscita_pct,
    ROW_NUMBER() OVER (PARTITION BY anno ORDER BY (SUM(assunti) + SUM(cessati)) * 100.0 / NULLIF(SUM(organico), 0) DESC) AS rank_turnover
FROM base
WHERE organico > 0
GROUP BY anno, ente, comparto, tipo_istituzione
ORDER BY anno DESC, rank_turnover
LIMIT 500
