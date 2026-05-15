# Notes

## Tecnico

- la fonte non espone un URL statico: il download avviene via `POST` su `/datipensioni/downloadFile`
- il source type `http_post_file` (toolkit#242) gestisce il download direttamente, senza script esterno
- `dataset.yml` usa quindi `type: http_post_file` con `post_data` per i parametri del form
- `scripts/download_raw.py` resta come riferimento storico (pattern cookie GET→POST se l'endpoint dovesse richiederlo)
- il file cumulativo reale contiene almeno un caso di riga corrotta con frammento HTML del bridge WebLogic; per questo il `clean.read` usa `strict_mode: false` e `ignore_errors: true`
- il v0 sceglie `2024` perche e l'ultimo anno completo nel cumulativo; `2025` parte solo da aprile
- il mart tiene lo snapshot `mese = 12` per evitare letture distorte da medie mensili su uno stock
- run locale eseguito il `2026-03-28`: raw, clean e mart prodotti correttamente
- shape clean verificata via `duckdb_describe`: `63.547` righe x `18` colonne
- shape mart verificata via `duckdb_describe`: `40` righe x `7` colonne
- rischio residuo di runtime: su Windows il comando `toolkit run all` chiude i layer ma fallisce nel rename finale del file `_runs/` con `WinError 5`; il bug sembra nel run record, non nel candidate
- notebook v0 eseguito - celle 1-4 con output testuali leggeri, cella 5 ok con output grafico non committato

## Metodologia di ingestion

- staging raw: `toolkit run raw` (source type `http_post_file`, fetch via POST)
- file scaricato: `Dati_Tipo_Pensione_totale.csv`
- filtro analitico v0:
  - `Anno = 2024`
  - `Mese = 12`
  - `Tipo Pensione in ('DIRETTA', 'INDIRETTA/REVERSIBILE')`
  - esclusi aggregati `Italia` ed `Estero`

## Analitico

- il file nasce a granularita ufficio/provincia, ma il primo mart sale a livello regionale
- il campo guida del v0 e `Numero Partite`
- gli importi restano nel clean per possibili estensioni, ma non guidano il primo output

## Cautele

- il dataset copre pensioni dello Stato gestite dal DAG, non il totale INPS
- i nomi territoriali della fonte non sono ancora normalizzati su codifiche ISTAT
- `Trentino-Sudtirol` e `Valle dAosta` vanno eventualmente armonizzati in uno step successivo
- il bug sporadico del bridge HTML va tenuto presente se il file cambia comportamento lato fonte
