# ga-decreti — Note tecniche

## Architettura

31 source CKAN paralleli, uno per sede. clean.sql usa `FROM raw_input` — il toolkit gestisce il merge multi-file con `read_csv([paths], union_by_name=true)`.

## Resource name matching

Il toolkit CKAN matcha `resource_name` come substring case-insensitive. Per le sedi con apostrofo Unicode (`L'Aquila`, `Valle d'Aosta`), il nome va scritto con U+2019.

## Run

```
toolkit run full --config candidates/ga-decreti/dataset.yml --years 2024
```

## Volumi

| Anno | Decreti | Sedi |
|---|---|---|
| 2023 | 2.601 | 31 |
| 2024 | 2.230 | 31 |
| 2025 | 1.727 | 31 |
| 2026 | 926 | 31 |

## Copertura mensile

OpenGA aggiorna i dataset ogni mese. Per l'aggiornamento schedulato, rieseguire il run full su tutti gli anni.
