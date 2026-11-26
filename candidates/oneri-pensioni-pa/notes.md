# Notes — oneri-pensioni-pa

## Tecnico

- Fonte: **MEF DAG**, open data "Amministrazione" / oneri (`datipensioni.mef.gov.it`).
- Download: `POST /datipensioni/downloadFile` con `categoria=oneri`, `filename=Dati_Amministrazione_YYYYMM.csv`, `dataset=DOWNLOAD_RDF_MESE_ANNO_ONERI`, `mese`, `anno`.
- `scripts/download_dag_oneri.py --year YYYY` scarica **dicembre**; il raw canonico resta in `out/`.
- Ogni file mensile: 384-412 righe, 5 Ministeri (6 dal 2022), 13-16 capitoli, 95 RTS (stessi codici della fonte `Tipo Pensione`).
- Il plugin `http_post_file` non templa `post_data`; per questo serve lo script (stesso pattern di `pensioni-pa-dag`).

## Metodologia

- **Dicembre** = snapshot di fine anno, confrontabile tra anni.
- Il mart include tutti i Ministeri, i capitoli e le RTS della fonte.
- `Importi ARRETRATI`, `RATEI`, `TREDICESIMA` sono componenti; `Importi TOTALE` è un totale pubblicato dalla fonte. È sempre ≥ della somma dei tre (verificato), ma **non è la loro somma**: non derivarlo.
- Il grano della fonte è Ministero × Capitolo × Piano di Gestione × RTS; il mart aggrega per Ministero e per RTS.

## Analitico

- 2024-12: 102.992 partite, 158,5 M€; MEF 84.611 partite (82%) e 111,2 M€; poi SALUTE, INTERNO, DIFESA, GIUSTIZIA, LAVORO.
- Le partite coincidono esattamente con `pensioni-pa-dag` dal 2018 al 2025. Nel **2017** i due file differiscono di 10 partite (R1 +9, CT +1): è una revisione della fonte, non un errore di pipeline.
- Il calo delle partite 2017-2025 è quello del perimetro pensioni; il costo va letto separatamente.

## Validazione

```bash
python candidates/oneri-pensioni-pa/scripts/check_oneri.py
```

- 0 duplicati sulla chiave, 0 nulli/negativi;
- `Importi TOTALE` ≥ componenti;
- 95 RTS;
- mart per Ministero e per RTS = clean (importi);
- cross-check partite con `pensioni-pa-dag` (se l'output è presente).

## Cautele

- Il dizionario della fonte per `Importi TOTALE` non è linkato nella pagina: da recuperare prima di usarlo come "spesa annua".
- Il form MEF non ha versioning: se cambia, il raw fallisce.
- `source_id: mef_dag` non è ancora in source-observatory (il radar elenca il perimetro sotto `inps`).
- Non sommare `Importi TOTALE` e i componenti: misurano cose diverse.
