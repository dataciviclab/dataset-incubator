# ga-decreti — Note tecniche

## Architettura

31 source CKAN paralleli, schema identico. clean.sql usa `FROM raw_input` (merge automatico multi-file del toolkit).

## Run

```
toolkit run full --config candidates/ga-decreti/dataset.yml --years 2024
```
