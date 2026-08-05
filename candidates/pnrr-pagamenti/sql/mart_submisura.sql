SELECT
    codice_univoco_submisura,
    descrizione_submisura,
    COUNT(DISTINCT cup) AS n_progetti,
    ROUND(SUM(finanziamento_totale)) AS tot_finanziamento,
    ROUND(SUM(finanziamento_pnrr)) AS tot_finanziamento_pnrr,
    ROUND(SUM(pagamento_totale)) AS tot_pagamenti,
    ROUND(SUM(pagamento_pnrr)) AS tot_pagamenti_pnrr,
    ROUND(SUM(pagamento_pnrr) / NULLIF(SUM(finanziamento_pnrr), 0) * 100, 2) AS tasso_assorbimento_pnrr_pct
FROM clean_input
GROUP BY codice_univoco_submisura, descrizione_submisura
