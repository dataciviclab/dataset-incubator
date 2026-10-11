# mase-prezzi-carburanti-settimanali

## Domanda civica

Quanto pesa l'accisa (e l'IVA) sul prezzo alla pompa di benzina e gasolio, e come
si è evoluto il carico fiscale sul litro dagli anni 2000 a oggi? Serie nazionale
settimanale con componente fiscale già scomposta.

## Dataset / fonte

MASE — DGSAIE (Statistiche energetiche), API open non catalogate su dati.gov.it:

`GET https://sisen.mase.gov.it/dgsaie/api/v1/weekly-prices/report/export?type=ALL&format=CSV&lang=it`

- CSV ISO-8859-1, delimiter `,`, decimali in `,` (campi quotati)
- Valori in **millesimi di euro** — clean converte in €/L
- Copertura: 2005-01 → ~settimana corrente, 8 prodotti (benzina, gasolio, GPL, gasolio riscaldamento, OC, metano/GNL dal 2023)

## Perché vale la pena

- Composizione fiscale prezzo (netto + accisa + IVA) in un'unica serie lunga
- Affianca ADM accertato: qui è prezzo/aliquota percepita, non gettito
- API stabile, un solo file, niente scraping

## Output minimo atteso

- Clean in €/L con `quota_accisa_pct`
- Mart = clean arricchito (serie pronta per analisi/trend)

## Criterio di promozione

- Readiness ready
- Benzina 2024 prezzo ~1,7–1,9 €/L e quota accisa plausibile (~40–50%)

## Stato / prossimo passo

- Branch: `intake/mase-prezzi-carburanti` (con `mase-prezzi-carburanti-mensili`)
- Prossimo: review PR, poi eventuale confronto con ADM
