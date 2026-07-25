-- ISPRA: Kg RU e RD pro-capite per provincia e anno
-- Produzione di rifiuti urbani e raccolta differenziata per abitante,
-- con confronto RD% e rapporto tra produzione totale e RD.
SELECT
    anno,
    regione,
    provincia,
    COUNT(*) AS comuni,
    ROUND(SUM(popolazione), 0) AS popolazione_totale,
    ROUND(SUM(totale_ru_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0), 1) AS kg_ru_procapite,
    ROUND(SUM(totale_rd_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0), 1) AS kg_rd_procapite,
    -- Quota di RD: calcolata sui kg (coerente con la % in peso)
    ROUND(SUM(totale_rd_tonnellate) * 100.0 / NULLIF(SUM(totale_ru_tonnellate), 0), 2) AS rd_pct_su_peso,
    ROW_NUMBER() OVER (PARTITION BY anno ORDER BY SUM(totale_ru_tonnellate * 1000.0) / NULLIF(SUM(popolazione), 0) DESC) AS rank_kg_ru
FROM clean_input
WHERE popolazione > 0
  AND provincia IS NOT NULL
GROUP BY anno, regione, provincia
ORDER BY anno DESC, rank_kg_ru
