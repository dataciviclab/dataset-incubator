# Notes — pensioni-pa-dag

## Tecnico

- Fonte: **MEF DAG**, open data "Tipo Pensione" (`datipensioni.mef.gov.it`).
- Il file cumulativo del v0 (`Dati_Tipo_Pensione_totale.csv`) **non è più servito**: la fonte risponde con una pagina HTML `NOME FILE NON CONSENTITO`. Ora pubblica solo file mensili `Dati_Tipo_Pensione_YYYYMM.csv`.
- Download riproducibile: `POST /datipensioni/downloadFile` con `categoria=pensioni`, `filename=Dati_Tipo_Pensione_YYYYMM.csv`, `dataset=DOWNLOAD_RDF_MESE_ANNO_PENS`, `mese`, `anno`.
- `scripts/download_dag.py --year YYYY` scarica **dicembre**; il raw canonico resta in `out/`.
- Il plugin `http_post_file` non templa `post_data` (`{year}` è sostituito solo nei valori di primo livello), per questo serve lo script.
- Ogni file mensile è uno snapshot: 5.078-7.525 righe (2017-12 → 2025-12), **22 territori** (20 regioni + Italia + Estero) e **95 uffici** in tutti gli anni.

## Metodologia

- **Dicembre** = stock di fine anno, confrontabile tra anni; il mart filtra `mese = 12`.
- Il mart include **tutti i territori**: le 20 regioni, l'ufficio centrale `Italia` (`ROMA - MEF DST UFFICIO V`) e `Estero`. Non sono aggregati: sono componenti reali dello stock.
- Include tutti i tipi: `DIRETTA`, `INDIRETTA/REVERSIBILE` e `UNA TANTUM` (1-2 partite nel 2017-2018/2022).
- La riga `Italia` **non è il totale nazionale**: è un ufficio (R1). Il totale è la somma di tutte le righe.
- Granularità della fonte: ufficio/provincia; il mart aggrega a territorio.

## Analitico

- Serie del mart: 9 anni (2017-2025). Totali: **180.168 (2017) → 95.990 (2025)**.
- 2024-12: 102.992 = 83.163 regioni + 18.083 Italia + 1.746 Estero.
- Per tipo (2024-12): `DIRETTA` 54.537, `INDIRETTA/REVERSIBILE` 48.455.
- Il calo è in entrambi i tipi; gli uffici sono 95 costanti, quindi non è un buco di copertura.
- Gli importi (arretrati, ratei, tredicesima, mensili) restano nel clean; il mart espone i mensili pagati.

## Validazione

```bash
python candidates/pensioni-pa-dag/scripts/check_dag.py
```

Controlli:
- identità `regioni + Italia + Estero = totale`;
- 0 duplicati sulla chiave naturale, 0 nulli/negativi;
- 22 territori e 95 uffici per anno;
- somma del mart = clean e una riga per `(anno, regione, tipo)` (44-45 righe/anno).

Cross-vintage: il mensile 2024-12 coincide col cumulativo storico 2024-12 (5.328 righe, 102.992 partite). Il cumulativo conteneva la riga corrotta WebLogic (2024-10) che il v0 mascherava con `ignore_errors`; i mensili non ne hanno bisogno.

**Cross-check con `oneri-pensioni-pa`**: gli oneri per amministrazione hanno le stesse partite di questo dataset (2018-2025 esatti; 2022-12: 119.068; 2024-12: 102.992; 2025-12: 95.990). Nel **2017** i due file differiscono di **10 partite** (R1 +9, CT +1): è una revisione della fonte, non un errore di pipeline.

## Cautele

- Il form MEF non ha versioning: se cambia, il raw fallisce (meglio un errore esplicito che un CSV vuoto).
- `source_id: mef_dag` non è ancora in source-observatory; il radar elenca il dataset sotto `inps`.
- Il perimetro è **DAG**, non INPS: non confrontare i totali con `open-inps` senza dichiararlo.
- Il calo 2017-2025 è nel dato; per una conferma esterna serve un report DAG ufficiale.
