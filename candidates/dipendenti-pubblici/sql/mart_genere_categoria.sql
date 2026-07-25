-- Dipendenti Pubblici: Quota donne per macrocategoria e anno
-- Gender gap nella PA: percentuale femminile per macrocategoria,
-- con delta anno su anno per vedere il trend
WITH base AS (
    SELECT
        anno,
        macrocategoria,
        -- totali per genere (full + part time)
        (donne_tempo_pieno + donne_part_time_inf_50 + donne_part_time_sup_50) AS donne_totali,
        (uomini_tempo_pieno + uomini_part_time_inf_50 + uomini_part_time_sup_50) AS uomini_totali
    FROM clean_input
    WHERE macrocategoria IS NOT NULL
)
SELECT
    anno,
    macrocategoria,
    ROUND(SUM(donne_totali + uomini_totali), 0) AS dipendenti_totali,
    ROUND(SUM(donne_totali), 0) AS donne,
    ROUND(SUM(uomini_totali), 0) AS uomini,
    ROUND(SUM(donne_totali) * 100.0 / NULLIF(SUM(donne_totali + uomini_totali), 0), 2) AS quota_donne_pct,
    ROUND((SUM(donne_totali) * 100.0 / NULLIF(SUM(donne_totali + uomini_totali), 0))
        - LAG(SUM(donne_totali) * 100.0 / NULLIF(SUM(donne_totali + uomini_totali), 0))
            OVER (PARTITION BY macrocategoria ORDER BY anno), 2)
        AS delta_quota_donne_pct
FROM base
GROUP BY anno, macrocategoria
ORDER BY anno DESC, dipendenti_totali DESC
