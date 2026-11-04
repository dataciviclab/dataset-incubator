# Codelists condivisi (ISTAT)

Tabelle di traduzione codice → etichetta, usate dai candidate con `support: file`
+ placeholder `{support.<name>.path}` (nessun path hardcoded nel SQL).

**Non sono dataset**: non hanno una domanda civica e non passano per la pipeline
registry. Sono file di appoggio versionati.

## `istat_territori.csv`

`ref_area, nome, livello` — gerarchia territoriale ISTAT.

- **Fonte**: codelist SDMX ISTAT `CL_ITTER107`
  (`https://esploradati.istat.it/SDMXWS/rest/codelist/IT1/CL_ITTER107/latest`, XML SDMX-ML 2.1)
- **Scope**: solo codici territoriali `IT*` (nazionale/ripartizione/regione/provincia
  + macro-aree), ~338 righe. **Comuni esclusi**: la gerarchia comunale completa
  (NUTS 2021/2024) è già in `compose/comuni-master`. Esclusi anche i codici **non
  territoriali** della codelist (ATO idrici, classi di ampiezza, `00`, …).
- **Livello**: codificato nella forma del codice (gerarchia standard):
  `IT` → nazionale · `IT[C-G]` → ripartizione · `IT[C-G][1-9]` → regione ·
  `IT[C-G][1-9][1-9]` o `IT[0-9]{3}` → provincia. Tutto il resto → `aggregato`
  (macro-aree `ITCD`/`ITFG`, `ITDA`, `ITZ`, `IT_C`, …), escluse dalle somme.

## `istat_cittadinanze.csv`

`codice, nome, tipo` — cittadinanza (ex-cittadinanza per `29_849`).

- **Fonte**: metadata DBnomics dei dataflow ISTAT `29_849` / `29_348` / `29_317`
  (etichette di fonte, unione dei tre).
- **`tipo`**: `paese` = foglia sommabile (ISO-2 + residui reali `X95`/`X94`/`X777`/
  Sud Sudan); `aggregato` = area geopolitica, `WORLD` o categoria sovrapposta (`999`).

## Rigenerazione

I file sono generati **offline** (non c'è ancora un fetch in pipeline: il toolkit
gestisce i codelist SDMX solo per Eurostat, non per ISTAT — l'endpoint ISTAT è XML).
La ricetta è nei commenti dei `dataset.yml` dei candidate e nella nota
`_local/notes/current/2026-11-03_IMMIGRAZIONE_FONTI_ISTAT.md`.

> Nota: se in futuro il toolkit estendesse `fetch_codelist` al profilo ISTAT,
> questi due file potrebbero diventare `support: codelist` (fetch dalla fonte).
