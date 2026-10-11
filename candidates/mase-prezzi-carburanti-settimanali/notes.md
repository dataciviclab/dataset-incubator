# notes — mase-prezzi-carburanti-settimanali

## Fonte

- Endpoint API SPA (non CKAN): `https://sisen.mase.gov.it/dgsaie/api/v1/weekly-prices/report/export?type=ALL&format=CSV&lang=it`
- Verificato open senza auth il 2026-10-11
- Encoding ISO-8859-1; DELIM `,`; decimali con `,` in campi quotati

## Unità di misura

- PREZZO/ACCISA/IVA/NETTO in **millesimi di euro** (1115,75 = 1,11575 €/L)
- clean divide per 1000 → suffisso `_eur`

## Quirk

- Metano e GNL partono ~2023 (serie breve)
- `VARIAZIONE` è delta sul prezzo totale rispetto alla settimana precedente, stesso ordine di grandezza millesimi
- IVA può essere 0 su prodotti con fiscalità agevolata/esente in certi periodi
- Non confondere con Osservaprezzi (prezzi per impianto, API diversa, auth)

## Limite semantico

- Media **nazionale** del prezzo praticato, non consumo e non gettito regionale

## mart_tagli_accisa

- Soglia 0,02 €/L su delta accisa settimanale per prodotto
- Cattura i tagli policy 2022 e 2026 e gli adeguamenti minimi
- `tipo_variazione` = taglio | aumento
