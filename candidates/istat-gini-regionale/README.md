# ISTAT Gini Regionale

Indice di Gini sul reddito netto regionale, con serie storica annuale.

## Domanda civica

Le disuguaglianze di reddito tra regioni italiane stanno convergendo o divergendo?

## Fonte

- **Ente**: ISTAT — Dataflow 32_221 (Omogeneita' del reddito regionale), DSD `DCCV_GINIREDD`
- **Endpoint**: `https://esploradati.istat.it/SDMXWS/rest`
- **Formato**: SDMX-CSV
- **Granularita**: regionale (ITTER107), serie storica annuale
- **Misura**: Indice di Gini sul reddito netto (`TIPO_DATO=DISUG_REDDNET_GINI`)

## Nota metodologica

Il dataflow distingue tra reddito con fitti imputati (`PRES_AFF_IMP=1`) e senza (`PRES_AFF_IMP=2`). In Italia la proprieta' della casa abbassa la disuguaglianza percepita sul reddito disponibile — la scelta va dichiarata esplicitamente.

## Perimetro v0

- Serie annuale per regione, ultimo decennio disponibile
- Colonne mart: anno, regione, gini, pres_aff_imp
- Entrambe le serie (con/senza fitti imputati), con documentazione della differenza
