-- IRPEF: Composizione del reddito per regione
-- Quota percentuale di ogni fonte di reddito (lavoro dip., pensione,
-- autonomo, fabbricati, partecipazione) sul reddito complessivo.
SELECT
    anno_di_imposta AS anno,
    regione,
    COUNT(*) AS comuni,
    -- Importi totali per fonte
    ROUND(SUM(reddito_da_fabbricati_eur), 0) AS fabbricati_eur,
    ROUND(SUM(reddito_da_lavoro_dipendente_e_assimilati_eur), 0) AS lavoro_dip_eur,
    ROUND(SUM(reddito_da_pensione_eur), 0) AS pensione_eur,
    ROUND(SUM(reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur), 0) AS lavoro_autonomo_eur,
    ROUND(SUM(reddito_da_partecipazione_eur), 0) AS partecipazione_eur,
    ROUND(SUM(reddito_complessivo_eur), 0) AS reddito_complessivo_totale,
    -- Quote percentuali
    ROUND(SUM(reddito_da_fabbricati_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS quota_fabbricati_pct,
    ROUND(SUM(reddito_da_lavoro_dipendente_e_assimilati_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS quota_lavoro_dip_pct,
    ROUND(SUM(reddito_da_pensione_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS quota_pensione_pct,
    ROUND(SUM(reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS quota_autonomo_pct,
    ROUND(SUM(reddito_da_partecipazione_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS quota_partecipazione_pct,
    -- Indicatore di dipendenza da pensione (proxy fragilita')
    ROUND(SUM(reddito_da_pensione_eur) * 100.0 / NULLIF(SUM(reddito_complessivo_eur), 0), 2) AS dipendenza_pensione_pct
FROM clean_input
WHERE regione IS NOT NULL
GROUP BY anno, regione
ORDER BY anno DESC, reddito_complessivo_totale DESC
