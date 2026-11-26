# Notes — pensioni-pa-dag

## Tecnico

- Fonte: **MEF DAG**, open data "Tipo Pensione" (`datipensioni.mef.gov.it`).
- Il file cumulativo del v0 (`Dati_Tipo_Pensione_totale.csv`) **non è più servito**: la fonte risponde con una pagina HTML `NOME FILE NON CONSENTITO`. Ora pubblica solo file mensili `Dati_Tipo_Pensione_YYYYMM.csv`.
- Download riproducibile: `POST /datipensioni/downloadFile` con `categoria=pensioni`, `filename=Dati_Tipo_Pensione_YYYYMM.csv`, `dataset=DOWNLOAD_RDF_MESE_ANNO_PENS`, `mese`, `anno`.
- `scripts/download_dag.py --year YYYY` scarica **dicembre** dell'anno; il raw canonico resta in `out/`.
- Il plugin `http_post_file` non templa `post_data` (`{year}` è sostituito solo nei valori di primo livello), per questo serve lo script.
- Ogni file mensile è uno snapshot: 5.078-7.525 righe (2017-12 → 2025-12), 22 territori (20 regioni + Italia + Estero).
- Il vecchio cumulativo locale in `inputs/` è obsoleto ed è ignorato da git; non è una fonte del run.

## Metodologia

- **Dicembre** = stock di fine anno, confrontabile tra anni; il mart filtra `mese = 12`.
- Tipi: `DIRETTA` e `INDIRETTA/REVERSIBILE`; `UNA TANTUM` (2017) è esclusa.
- Esclusi gli aggregati `Italia` ed `Estero`.
- **La riga `Italia` non è il totale nazionale** (2024-12: 18.083 contro 102.992 sommando le regioni): non usarla come denominatore.
- Granularità della fonte: ufficio/provincia; il mart aggrega a regione.

## Analitico

- Serie del mart: 9 anni (2017-2025), 40 righe/anno (20 regioni × 2 tipi).
- `numero_partite` nel mart: 158.892 (2017) → 76.339 (2025). Il calo è nel perimetro DAG, non nel totale INPS.
- Gli importi (arretrati, ratei, tredicesima, mensili) restano nel clean; il mart espone i mensili pagati.

## Cautele

- Il form MEF non ha versioning: se cambia, il raw fallisce (meglio un errore esplicito che un CSV vuoto).
- `source_id: mef_dag` non è ancora in source-observatory; il radar elenca il dataset sotto `inps`.
- Il perimetro è **DAG**, non INPS: non confrontare i totali con `open-inps` senza dichiararlo.
- Non sommare la riga `Italia` alle regioni.
