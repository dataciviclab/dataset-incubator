# opencivitas-glossario — Note

## Origine

File XLSX di metadati estratti da OpenCivitas: `{year}_Metadati_Ind_FC{code}_{n}_xlsx.zip`.
Ogni file contiene 3 fogli: Indicatori, Determinanti, Codici.

## Pipeline

```
preprocess.py {year} raw_input.csv
  → download 7 XLSX (uno per ambito)
  → estrae 3 fogli da ciascuno
  → unisce in CSV unico con colonne: codice_indicatore, descrizione, tipo, categoria, funzione, ordine, anno, ambito

clean.sql → pass-through (normalizza trim/cast)

mart.sql → pass-through (select * from clean_input)
```

## Anni

7 anni: 2015, 2016, 2017, 2018, 2019, 2021, 2022.
(2020 assente: nessun indicatore pubblicato.)

## Note

- 2015: URL senza anno e suffisso 2 (es. `Metadati_Ind_FC20AMMIN_2_xlsx.zip`)
- 2016-2022: URL standard con anno e suffisso 1
- I determinanti (DET) e i codici (COD) variano per anno
- Il candidate referenzia il mart via `{root}/data/mart/opencivitas_glossario/{year}/mart_metadati.parquet`
