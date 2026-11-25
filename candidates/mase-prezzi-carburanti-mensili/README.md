# mase-prezzi-carburanti-mensili

## Domanda civica

Come si è mossa la componente fiscale (accisa + IVA) sul prezzo della benzina e
del gasolio negli ultimi 30 anni? Serie mensile lunga utile a contestualizzare
shock energetici e variazioni di aliquota.

## Dataset / fonte

MASE — DGSAIE, API open:

`GET https://sisen.mase.gov.it/dgsaie/api/v1/monthly-prices/export?format=CSV&lang=it`

- Copertura: **1996 → 2026**, 8 prodotti
- Stessa grammatica della serie settimanale (millesimi di euro → €/L in clean)
- Nel file ci sono anche righe Anno/Trimestre (`CODICE_MESE` 13–17): escluse dal clean

## Perché vale la pena

- Serie lunga e stabile per trend strutturali del carico fiscale
- Complementare al candidate settimanale (bassa frequenza, storico profondo)

## Output minimo atteso

- Clean mensile in €/L con `quota_accisa_pct`, PK (anno, mese, prodotto)
- Mart = clean

## Criterio di promozione

- Readiness ready
- Prezzi benzina 1996 e 2024 in range plausibili ( conversione /1000 corretta)

## Stato / prossimo passo

- Branch: `intake/mase-prezzi-carburanti` (con `mase-prezzi-carburanti-settimanali`)
