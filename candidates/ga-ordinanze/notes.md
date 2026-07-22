# ga-ordinanze — Note tecniche

## Architettura

31 source CKAN paralleli, uno per sede. clean.sql usa `FROM raw_input` — il toolkit gestisce il merge multi-file con `read_csv([paths], union_by_name=true)`.

## Resource name matching

Il toolkit CKAN matcha `resource_name` come substring case-insensitive. Per le sedi con apostrofo Unicode (`L'Aquila`, `Valle d'Aosta`), il nome va scritto con U+2019 (RIGHT SINGLE QUOTATION MARK), non ASCII.

## Run

```
toolkit run full --config candidates/ga-ordinanze/dataset.yml --years 2024
```

## Volumi

| Anno | Ordinanze | Sedi |
|---|---|---|
| 2023 | 4.796 | 31 |
| 2024 | 4.327 | 31 |
| 2025 | 3.970 | 31 |
| 2026 | 1.961 | 31 |

## Copertura mensile

OpenGA aggiorna i dataset ogni mese. Per l'aggiornamento schedulato, rieseguire il run full su tutti gli anni.
