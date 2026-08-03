-- mart_trend_anno — Finanziamenti UE diretti in Italia per anno (multi-year)
--
-- 1 riga = 1 anno: grant, importo contrattato totale, consumato, quota
-- assorbimento. RRF (Recovery) escluso dal totale analitico ma esposto
-- come colonna separata (is_rrf='SI') — trasferimenti di bilancio UE→Stato,
-- non grant analitici. Risponde: quanto vale l'UE per l'Italia? (D1, D9)
--
-- PK: (anno)

WITH per_anno AS (
    SELECT
        anno,
        count(*) FILTER (WHERE is_rrf = 'NO')                    AS n_grant,
        count(DISTINCT beneficiario_nome) FILTER (WHERE is_rrf = 'NO') AS n_beneficiari_distinti,
        sum(importo_contrattato) FILTER (WHERE is_rrf = 'NO' AND importo_contrattato IS NOT NULL) AS importo_contrattato_totale,
        -- Consumato a livello BENEFICIARIO (Beneficiary's estimated consumed).
        -- NOTA: NON usare impegno_consumato (Commitment consumed) — è il consumo
        -- dell'intero commitment, non della quota del beneficiario → ratio > 100%.
        sum(importo_consumato_stimato) FILTER (WHERE is_rrf = 'NO' AND importo_consumato_stimato IS NOT NULL) AS importo_consumato_totale,
        sum(importo_contrattato) FILTER (WHERE is_rrf = 'SI' AND importo_contrattato IS NOT NULL) AS importo_rrf_eur
    FROM clean_input
    WHERE anno IS NOT NULL
    GROUP BY anno
)
SELECT
    anno,
    n_grant,
    n_beneficiari_distinti,
    round(importo_contrattato_totale, 0)                            AS importo_contrattato_totale,
    round(importo_consumato_totale, 0)                              AS importo_consumato_totale,
    round(importo_rrf_eur, 0)                                       AS importo_rrf_eur,
    round(100.0 * importo_consumato_totale / NULLIF(importo_contrattato_totale, 0), 1)
                                                                    AS quota_consumato_pct,
    round(importo_contrattato_totale - lag(importo_contrattato_totale) OVER (ORDER BY anno), 0)
                                                                    AS delta_contrattato_eur,
    round(100.0 * (importo_contrattato_totale - lag(importo_contrattato_totale) OVER (ORDER BY anno))
          / NULLIF(lag(importo_contrattato_totale) OVER (ORDER BY anno), 0), 2)
                                                                    AS variazione_pct
FROM per_anno
ORDER BY anno
