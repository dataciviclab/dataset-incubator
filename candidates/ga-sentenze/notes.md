# ga-sentenze — Note tecniche

## Architettura

31 source CKAN paralleli, uno per sede. Il clean.sql usa `read_csv_auto` con glob `{year}/*.csv` e `union_by_name=true` per fondere automaticamente tutti i file.

## Resource name matching

Il toolkit CKAN matcha `resource_name` come substring case-insensitive. Per le sedi con apostrofo Unicode (`L'Aquila`, `Valle d'Aosta`), il nome va scritto con U+2019 (RIGHT SINGLE QUOTATION MARK), non ASCII.

## Drop colonne raw

- `ANNO_PUBBLICAZIONE` → rinominato in `anno` nel clean
- `_id` → auto-generato da DataStore, drop senza conseguenze

## Run

```
toolkit run full --config candidates/ga-sentenze/dataset.yml --years 2024
```

## Copertura mensile

OpenGA aggiorna i dataset ogni mese. Per l'aggiornamento schedulato, rieseguire il run full su tutti gli anni.

## Performance

31 file CSV × 4 anni ≈ 5-7 minuti totali (dipende dalla rete). Il clean merge via glob è istantaneo una volta che i raw sono disponibili.
