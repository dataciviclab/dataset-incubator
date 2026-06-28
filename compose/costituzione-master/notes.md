# costituzione-master

**Dataset derivato**: JOIN tra i 4 parquet di `dataciviclab/costituzione-italiana`.

Ogni riga = un articolo (1-139) con metriche aggregate da:
- `articoli.parquet` → testo, parte, heading
- `revisioni.parquet` → quante modifiche ha subito
- `atti-promovimento.parquet` → quante volte evocato in giudizio
- `indicatori-costituzionali.parquet` → quanti dataset Lab lo misurano

## Dipendenza

Lo script RAW scarica i parquet da `raw.githubusercontent.com/dataciviclab/costituzione-italiana`.
Il repo è pubblico — nessun token richiesto.

## Esecuzione

```bash
cd dataset-incubator
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run full \
  --config compose/costituzione-master/dataset.yml \
  --years 2026
```
