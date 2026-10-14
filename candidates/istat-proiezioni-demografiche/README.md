# ISTAT Proiezioni demografiche 2025–2080

## Domanda

- Quanti saremo in Italia nel 2050 e nel 2080?
- Come cambia il bilancio demografico (nati, morti, saldi)?

## Dataset

- fonte: [demo.istat.it](https://demo.istat.it/app/?i=PPR&l=it) — piattaforma tematica ISTAT
- canale: **SPA API** (`RPCCerca.php`) — niente SDMX (flaky)
- base: 1° gennaio 2025 · orizzonte: 2080
- scenario mediano + intervalli confidenza (50/80/90%)
- territori: Italia + 5 ripartizioni + 21 regioni NUTS2
- componenti: popolazione, nati, morti, saldo naturale, saldo migratorio

## Perché vale la pena

- dati ufficiali ISTAT, aggiornati annualmente
- unico dataset che copre l'intero orizzonte 2050–2080
- canale stabile (API JSON, no rate-limit ISTAT)

## Output

- `mart_popolazione_anno`: popolazione proiettata per territorio × anno
- `mart_componenti_anno`: nati, morti, saldi per territorio × componente × anno

## Canale

`preprocess.py` fa POST a `RPCCerca.php` (form-1: componenti bilancio).
SDMX IstatData (`165_889`) resta come alternativa documentata in notes.md.
