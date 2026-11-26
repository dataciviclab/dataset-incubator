# Oneri Pensioni PA — amministrazioni

**Oneri pensionistici DAG per amministrazione, capitolo di bilancio e RTS — dicembre 2017-2025**

## Domanda civica

Quali amministrazioni sostengono gli oneri delle pensioni gestite dalla DAG, e come si distribuisce il costo tra Ministeri, capitoli di bilancio e uffici territoriali? È il lato **finanziario** dello stesso stock raccontato da `pensioni-pa-dag`.

## Dataset

- **Fonte**: MEF — DAG, open data "Amministrazione" / oneri (`datipensioni.mef.gov.it`)
- **Canale**: POST form-encoded su `/datipensioni/downloadFile`; file mensili `Dati_Amministrazione_YYYYMM.csv`
- **Script**: `scripts/download_dag_oneri.py --year YYYY` (scarica dicembre)
- **Periodo**: dicembre 2017-2025 (9 snapshot annuali)
- **Licenza**: CC BY 4.0 (verificata sulla pagina di download: <https://creativecommons.org/licenses/by/4.0/deed.it>)

## Perché vale la pena

- È lo **stesso stock** di `pensioni-pa-dag` (le partite coincidono), ma letto per **Ministero, capitolo di bilancio e RTS**: chi paga e quanto.
- Complementa la vista territoriale con la dimensione di **spesa**.
- Permette di seguire il costo per amministrazione e la sua distribuzione territoriale.

## Output minimo atteso

- Clean: 13 colonne (anno, mese, ministero, capitolo, piano di gestione, RTS, partite, importi).
- `mart_oneri_per_ministero`: anno × ministero, partite, importi, quota % dell'anno.
- `mart_oneri_per_rts`: anno × RTS, partite, importi, quota % dell'anno.

## Perimetro e numeri

- Tutti i Ministeri, i capitoli e le 95 RTS della fonte.
- 2024-12: **102.992 partite**, **158,5 M€** di `Importi TOTALE`; il MEF da solo 84.611 partite (82%) e 111,2 M€.
- `Importi TOTALE` è un totale **pubblicato dalla fonte**: è sempre ≥ arretrati + ratei + tredicesima, ma non è la loro somma (include altre voci, probabilmente le mensilità). Non derivarlo.
- Le partite coincidono con `pensioni-pa-dag` (2022-12: 119.068; 2024-12: 102.992; 2025-12: 95.990).

## Validazione

```bash
python candidates/oneri-pensioni-pa/scripts/check_oneri.py
```

Controlla: 0 duplicati sulla chiave, 0 nulli/negativi, `Importi TOTALE` ≥ componenti, 95 RTS, mart = clean, e **cross-check partite con `pensioni-pa-dag`**.

## Criterio di promozione

- Serie dicembre 2017-2025 leggibile per Ministero e RTS.
- Semantica di `Importi TOTALE` chiarita con il dizionario della fonte.
- `source_id: mef_dag` registrato in `source-observatory`.

## Stato

`candidate` v1 — run 2017-2025, 9 partizioni, validazione incrociata con `pensioni-pa-dag`.

## Prossimo passo

- Recuperare il dizionario della fonte per `Importi TOTALE`.
- Registrare `mef_dag` in source-observatory.
- Valutare un join con `pensioni-pa-dag` per la lettura stock + costo.
