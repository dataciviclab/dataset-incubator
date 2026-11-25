-- Serie mensile 1996-2026 in €/L, solo mesi reali (no aggregati trimestrali/annuali).

SELECT
    anno,
    mese,
    nome_mese,
    codice_prodotto,
    prodotto,
    prezzo_eur,
    accisa_eur,
    iva_eur,
    netto_eur,
    quota_accisa_pct
FROM clean_input
