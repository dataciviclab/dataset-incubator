# ISTAT VA per branca — Conti territoriali

## Domanda

- Come si distribuisce il Valore Aggiunto per settore NACE nelle regioni italiane?
- Quale quota del VA regionale arriva dalla manifattura o dai servizi?

## Dataset

- fonte: ISTAT via DBnomics (`type: dbnomics`)
- dataflow: `93_1227_DF_DCCN_TNA1_1`
- indicatore: VA (`B1G_B_W2_S1`), valutazione corrente (`V`) e costanti 2020 (`L_2020`)
- grano: 21 regioni NUTS1 × NACE sezioni A–S (esclusa Z)
- unità: milioni di euro
- edizione pin: `2025M6`

## Perché vale la pena

- copertura storica lunga (1995–2023)
- complemento a `istat-pil-territoriale` (aggregate) e `eurostat_gva_nuts3`
- share per settore calcolato nel mart

## Output

- `mart_va_branca`: VA per regione × NACE × anno
- `mart_va_branca_share`: share % sul totale regionale
