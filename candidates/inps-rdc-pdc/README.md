# inps-rdc-pdc — Nuclei percettori RDC/PDC per comune (2020)

**Dataset**: nuclei familiari percettori di Reddito di Cittadinanza (RdC) e Pensione di Cittadinanza (PdC) per comune ISTAT, luglio 2020.

**Fonte**: INPS Open Data — CSV diretto
https://servizi2.inps.it/docallegati/Mig/OpenData/CSV/ID-5773.csv

**Issue**: [#435](https://github.com/dataciviclab/dataset-incubator/issues/435)

## Domanda guida

In quali comuni l'incidenza dei nuclei RdC/PdC è più alta rispetto alla popolazione? Come si correla col reddito medio dichiarato (IRPEF) e con altri indicatori socio-economici del Lab?

## Dataset

- **Copertura**: luglio 2020 (singolo snapshot)
- **Granularità**: comune ISTAT (7.976 comuni)
- **Join key**: `codice_istat` — join score 100/100 con 18 dataset del Lab
- **Colonne**: 19 (anno, codice_istat, comune, RdC, PdC, individui coinvolti, importo medio, takeup, popolazione, ecc.)
- **Formato clean**: Parquet, 19 colonne, 7.976 righe

## Perché vale la pena

- Dato unico sulla povertà assoluta a livello comunale
- Si aggancia perfettamente al catalogo esistente (popolazione, IRPEF, rifiuti, consumo suolo, FSC, dipendenti pubblici, AIFA, Consip, Terna)
- RdC/PdC è stato il principale strumento di contrasto alla povertà in Italia (2019-2023)

## Output minimo atteso

- Dataset clean `inps_rdc_pdc_2020_clean.parquet` queryabile via DuckDB
- Mart con dati comunali pronti per join
- Analisi territoriale: mappa takeup per comune, correlazione con IRPEF

## Criterio di promozione

- Run full passato (RAW→CLEAN→MART), readiness 5/5
- Dati coerenti: 7.976 comuni, importi e takeup realistici

## Limitazioni note

- **Singolo anno (2020)**: è l'unico snapshot comunale pubblicato da INPS in questo formato. Esistono dati regionali 2019-2023 sul portale CKAN INPS ma non comunali.
- **Nomi comuni**: in lowercase senza spazi (es. "abanoterme") — così nel dataset INPS originale. Il join è via `codice_istat`.
- **Comuni soppressi**: alcuni codici ISTAT (es. A042 Acquarica del Capo) hanno popolazione 0 perché fusi prima del 2020.
- **Importo medio con 0 nuclei**: 620 comuni hanno importo medio > 0 ma 0 nuclei RdC+PdC — artefatto del dato INPS originale.

## Stato

- ✅ Run full passato (RAW→CLEAN→MART)
- ✅ 7.976 righe, 19 colonne
- ✅ Readiness 5/5
- ⏳ Da pubblicare su explorer

## Prossimo passo

- Notebook v0 esplorativo
- Analisi pubblica in `dataciviclab/analisi/`
- Pubblicazione su data-explorer
