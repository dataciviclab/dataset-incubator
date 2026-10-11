-- Rilevamento discontinuità di accisa tra settimane consecutive, per prodotto.
-- Soglia: variazione assoluta >= 0.02 €/L (tagli policy 2022/2026 sono ~0,10–0,20).

WITH ordered AS (
    SELECT
        data_rilevazione,
        codice_prodotto,
        prodotto,
        accisa_eur,
        prezzo_eur,
        LAG(data_rilevazione) OVER w AS data_prec,
        LAG(accisa_eur) OVER w AS accisa_prec,
        LAG(prezzo_eur) OVER w AS prezzo_prec
    FROM clean_input
    WINDOW w AS (PARTITION BY codice_prodotto ORDER BY data_rilevazione)
),
diffs AS (
    SELECT
        data_rilevazione AS data_taglio,
        data_prec,
        codice_prodotto,
        prodotto,
        accisa_prec,
        accisa_eur AS accisa_nuova,
        accisa_eur - accisa_prec AS delta_accisa,
        prezzo_prec,
        prezzo_eur AS prezzo_dopo,
        prezzo_eur - prezzo_prec AS delta_prezzo,
        CASE
            WHEN accisa_eur < accisa_prec THEN 'taglio'
            WHEN accisa_eur > accisa_prec THEN 'aumento'
        END AS tipo_variazione
    FROM ordered
    WHERE accisa_prec IS NOT NULL
      AND ABS(accisa_eur - accisa_prec) >= 0.02
)
SELECT *
FROM diffs
ORDER BY codice_prodotto, data_taglio
