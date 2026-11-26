# Pensioni PA DAG

**Stock delle pensioni dello Stato gestite dalla DAG (MEF) — dicembre 2017-2025**

## Domanda civica

Come si distribuisce territorialmente lo stock di pensioni dello Stato gestite dalla DAG, e come cambia la composizione tra trattamenti diretti e indiretti/reversibili tra territori?

## Dataset

- **Fonte**: MEF — DAG, open data "Tipo Pensione" (`datipensioni.mef.gov.it`)
- **Canale**: POST form-encoded su `/datipensioni/downloadFile`; la fonte pubblica file **mensili** `Dati_Tipo_Pensione_YYYYMM.csv`
- **Script**: `scripts/download_dag.py --year YYYY` (scarica dicembre dell'anno)
- **Periodo**: dicembre 2017-2025 (9 snapshot annuali)
- **Licenza**: CC BY 4.0 (verificata sulla pagina di download: <https://creativecommons.org/licenses/by/4.0/deed.it>)

## Perché vale la pena

- Perimetro **distinto da INPS**: pensioni dello Stato gestite dalla DAG, non il totale delle pensioni italiane.
- Granularità: ufficio/provincia, tipo di pensione, microqualifica, titolo.
- Serie 2017-2025 per la domanda territoriale, con un taglio di fine anno confrontabile.

## Output minimo atteso

- Clean: 18 colonne (territorio, ufficio, tipo, microqualifica, titolo, partite, importi).
- `mart_territori_dicembre`: `anno`, `mese`, `regione`, `tipo_pensione`, `numero_partite`, `importi_mensili_pagati_eur`, `righe_granulari`.
- Include **20 regioni + ufficio centrale "Italia" (ROMA - MEF DST UFFICIO V) + Estero**, e tutti i tipi (`DIRETTA`, `INDIRETTA/REVERSIBILE`, `UNA TANTUM` trascurabile).

## Perimetro e numeri

- 2024-12: **102.992 partite** = 83.163 regioni + 18.083 Italia + 1.746 Estero.
- Serie totale del mart: **180.168 (2017) → 95.990 (2025)**; 22 territori e 95 uffici in tutti gli anni.
- `Italia` **non è un aggregato**: è l'ufficio centrale di Roma; `Estero` sono uffici reali. Il mart li include, quindi la sua somma coincide col totale del clean.
- Il calo è nel dato, non nella copertura (95 uffici costanti). Va confermato con un report ufficiale DAG.

## Validazione

```bash
python candidates/pensioni-pa-dag/scripts/check_dag.py
```

Controlla: identità `regioni + Italia + Estero = totale`, 0 duplicati sulla chiave naturale, 0 nulli/negativi, 22 territori e 95 uffici, somma del mart = clean e una riga per `(anno, regione, tipo)`.

Controlli già eseguiti:
- mensile 2024-12 vs cumulativo storico 2024-12: stesse 5.328 righe e 102.992 partite;
- cross-check con `oneri-pensioni-pa`: stesse partite (2022-12: 119.068; 2024-12: 102.992; 2025-12: 95.990);
- 9 anni 2017-2025: validazione OK, readiness 8/8;
- nessun negativo/zero anomalo nel 2024.

## Criterio di promozione

- Serie dicembre 2017-2025 leggibile, validata e documentata.
- `source_id: mef_dag` registrato in `source-observatory` (oggi il dataset è ancora elencato sotto `inps`).

## Stato

`candidate` v1 — run 2017-2025: 9 partizioni, mart validato, readiness 8/8.

## Prossimo passo

- Monitorare il form MEF: non ha versioning, se cambia il run fallisce nel raw.
- Registrare `mef_dag` in source-observatory.
- Confronto esterno con un report DAG ufficiale.
