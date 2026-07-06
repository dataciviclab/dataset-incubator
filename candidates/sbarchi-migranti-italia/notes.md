# sbarchi-migranti-italia

## Issue
DataCivicLab/dataset-incubator#596

## Fonte dati
Repository GitHub ondata/liberiamoli-tutti → `sbarchi-migranti/dati/`
https://github.com/ondata/liberiamoli-tutti/tree/main/sbarchi-migranti/dati

## File raw
- `sbarchi-per-giorno.csv`: arrivi giornalieri (settembre 2019–settembre 2025)

## Encoding
UTF-8, delimitatore virgola, header presente.

## Note
I campi Data nel CSV hanno formati misti (YYYY-MM-DD e DD/MM/YYYY).
TRY_CAST in DuckDB gestisce entrambi automaticamente.
