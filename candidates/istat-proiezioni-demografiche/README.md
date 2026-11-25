# ISTAT Proiezioni demografiche 2025–2080

## Domanda

- Quanti saremo in Italia nel 2050 e nel 2080?
- Come cambia la struttura per età e sesso?

## Dataset

- fonte: [demo.istat.it](https://demo.istat.it/app/?i=PPR&l=it) — ZIP ufficiale ISTAT
- file: `Previsioni-Popolazione_per_eta-Regioni.zip`
- base: 1° gennaio 2025 · orizzonte: 2080
- scenario mediano
- grano: 22 regioni NUTS2 × sesso × età (0–110+) × anno

## Perché vale la pena

- dati ufficiali ISTAT, aggiornati annualmente
- unico dataset che copre l'intero orizzonte 2050–2080
- canale stabile (ZIP statico, no rate-limit)

## Output

- `mart_regioni`: popolazione per regione × sesso × età × anno
- `mart_italia`: popolazione Italia (somma regioni) × sesso × età × anno
