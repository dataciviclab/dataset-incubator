# ISTAT ASIA — Imprese attive e addetti per settore

## Domanda

- Quante imprese attive e addetti ci sono per settore NACE in Italia e nelle regioni?
- Come si distribuiscono le imprese tra manifattura, costruzioni e servizi?

## Dataset

- fonte: ISTAT via DBnomics (`type: dbnomics`)
- dataflow: `183_277_DF_DICA_ASIAUE1P_1`
- indicatori: imprese attive (`AENTN`), addetti media annua (`AENTEMPDAA`)
- grano: Italia + 21 regioni NUTS1 × NACE totale/sezioni B–S
- filtri: forma giuridica totale, imprese con addetti, esclusi artigiani

## Perché vale la pena

- contatore di imprese per settore e territorio, base per densità imprenditoriale
- serie storica 2012–2024
- complemento a SBS (valori monetari) e VA branca

## Output

- `mart_asia_imprese_anno`: `anno × territorio × NACE × indicatore`
