-- Serie settimanale pronta all'uso: una riga per data x prodotto.
-- quota_accisa_pct = accisa sul prezzo totale (non sull'imponibile).

SELECT
    data_rilevazione,
    codice_prodotto,
    prodotto,
    prezzo_eur,
    accisa_eur,
    iva_eur,
    netto_eur,
    variazione_eur,
    quota_accisa_pct
FROM clean_input
