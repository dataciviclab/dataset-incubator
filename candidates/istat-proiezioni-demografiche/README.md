# ISTAT Proiezioni demografiche 2025–2080

## Domanda

- Quanti saremo in Italia nel 2050 e nel 2080?
- Come cambia la struttura per età e sesso?
- Quali regioni perdono più popolazione?

## Dataset

- fonte: ISTAT IstatData, dataflow `165_889` (`DCIS_PREVDEM1`)
- base: 1° gennaio 2025 · orizzonte: 2080
- scenario mediano + intervalli di confidenza (50/80/90%)
- grano: IT + regioni NUTS2 × sesso × età × anno
- comunicato: [ISTAT 2026](https://www.istat.it/comunicato-stampa/previsioni-della-popolazione-residente-delle-famiglie-e-delle-forze-di-lavoro-base-1-1-2025/)
- anche su [demo.istat.it (PPR)](https://demo.istat.it/app/?i=PPR) — SPA, non scaricabile via HTTP diretto

## Perché vale la pena

- dati ufficiali ISTAT, aggiornati annualmente
- base per qualsiasi analisi di welfare, pensioni, sanità, lavoro
- unico dataset che copre l'intero orizzonte 2050–2080

## Note operative

- SDMX ISTAT è **flaky** (timeout/redirect). Se il run fallisce, riprovare.
- Il clean filtra IT + regioni; adattare lo scenario dopo il primo run (dipende dal DSD).
- Complemento: `bilancio-demografico` (22_315) per i flussi osservati.

## Output

- `mart_proiezioni_anno`: popolazione per territorio × sesso × età × anno
- `mart_proiezioni_ripartizione`: aggregato Nord / Centro / Sud e Isole
