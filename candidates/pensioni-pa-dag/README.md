# Pensioni PA DAG

**Stock delle pensioni dello Stato gestite dalla DAG (MEF) — snapshot di dicembre 2017-2025**

## Domanda civica

Come si distribuisce territorialmente lo stock di pensioni dello Stato gestite dalla DAG, e come cambia la composizione tra trattamenti diretti e indiretti/reversibili tra regioni?

## Dataset

- **Fonte**: MEF — DAG, open data "Tipo Pensione" (`datipensioni.mef.gov.it`)
- **Canale**: POST form-encoded su `/datipensioni/downloadFile`; la fonte pubblica file **mensili** `Dati_Tipo_Pensione_YYYYMM.csv`
- **Script**: `scripts/download_dag.py --year YYYY` (scarica dicembre dell'anno)
- **Periodo**: dicembre 2017-2025 (9 snapshot annuali)
- **Licenza**: CC BY 4.0 (dichiarata dalla fonte)

## Perché vale la pena

- Perimetro **distinto da INPS**: pensioni dello Stato gestite dalla DAG, non il totale delle pensioni italiane.
- Granularità: ufficio/provincia, tipo di pensione, microqualifica, titolo.
- Serie 2017-2025 per la domanda territoriale, con un taglio di fine anno confrontabile.

## Output minimo atteso

- Clean: 18 colonne (territorio, ufficio, tipo, microqualifica, titolo, partite, importi).
- `mart_regioni_dicembre`: `anno`, `mese`, `regione`, `tipo_pensione`, `numero_partite`, `importi_mensili_pagati_eur`, `righe_granulari`.
- 9 anni × 20 regioni × 2 tipi.

## Perimetro v0

- Solo **dicembre** (stock di fine anno), solo `DIRETTA` e `INDIRETTA/REVERSIBILE`.
- Esclusi gli aggregati `Italia` ed `Estero`.
- La riga `Italia` **non è il totale nazionale** (2024-12: 18.083 contro 102.992 sommando le regioni): va esclusa.
- `UNA TANTUM` (presente nel 2017) è esclusa dal mart.

## Criterio di promozione

- Serie dicembre 2017-2025 leggibile e documentata.
- `source_id: mef_dag` registrato in `source-observatory` (oggi il dataset è ancora elencato sotto `inps`).

## Stato

`candidate` v1 — run 2017-2025: 9 partizioni, mart 40 righe/anno, readiness 8/8.

## Prossimo passo

- Monitorare il form MEF: non ha versioning, se cambia il run fallisce nel raw.
- Registrare `mef_dag` in source-observatory.
- Valutare un dettaglio per microqualifica o l'estensione a tutti i mesi.
