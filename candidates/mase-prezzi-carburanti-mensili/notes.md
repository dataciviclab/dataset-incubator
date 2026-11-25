# notes — mase-prezzi-carburanti-mensili

## Fonte

- `https://sisen.mase.gov.it/dgsaie/api/v1/monthly-prices/export?format=CSV&lang=it`
- Open no auth (verificato 2026-10-11); ISO-8859-1; delim `,`; decimali `,`

## Pulizia

- Solo `CODICE_MESE` 1–12 (13=Anno, 14–17=Trimestre esclusi)
- Valori /1000 → euro

## Quirk

- Prodotti 6/8 (oli combustibili) hanno IVA agevolata/zero in certi anni
- Metano/GNL da ~2023
- Formato "EXCEL" dell'API è in realtà CSV con `;` — usiamo `format=CSV`

## Limite semantico

- Media nazionale mensile del prezzo, non consumo né gettito
