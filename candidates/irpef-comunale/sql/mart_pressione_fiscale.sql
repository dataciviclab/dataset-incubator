-- IRPEF: Pressione fiscale locale per comune
-- Aliquota effettiva media (imposta netta / reddito imponibile)
-- e addizionale comunale effettiva per comune e regione.
SELECT
    anno_di_imposta AS anno,
    regione,
    sigla_provincia AS provincia,
    codice_istat_comune,
    denominazione_comune AS comune,
    numero_contribuenti,
    ROUND(reddito_imponibile_eur, 0) AS reddito_imponibile_totale,
    ROUND(imposta_netta_eur, 0) AS imposta_netta_totale,
    ROUND(addizionale_comunale_dovuta_eur, 0) AS addizionale_comunale_totale,
    -- Aliquota effettiva media (imposta netta / reddito imponibile)
    ROUND(imposta_netta_eur * 100.0 / NULLIF(reddito_imponibile_eur, 0), 2) AS aliquota_effettiva_pct,
    -- Addizionale comunale effettiva
    ROUND(addizionale_comunale_dovuta_eur * 100.0 / NULLIF(reddito_imponibile_eur, 0), 2) AS addizionale_effettiva_pct,
    -- Reddito medio per contribuente
    ROUND(reddito_imponibile_eur / NULLIF(numero_contribuenti, 0), 0) AS reddito_medio_per_contribuente,
    -- Ranking regionale per aliquota
    ROW_NUMBER() OVER (PARTITION BY anno_di_imposta, regione ORDER BY imposta_netta_eur * 100.0 / NULLIF(reddito_imponibile_eur, 0) DESC) AS rank_aliquota_in_regione
FROM clean_input
WHERE regione IS NOT NULL
  AND reddito_imponibile_eur > 0
  AND numero_contribuenti > 0
ORDER BY anno DESC, aliquota_effettiva_pct DESC
