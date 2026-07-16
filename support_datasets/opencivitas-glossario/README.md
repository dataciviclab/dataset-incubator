# opencivitas-glossario

**Dizionario degli indicatori, determinanti e codici OpenCivitas.**

Unisce i 3 fogli dei file XLSX di metadati (`{year}_Metadati_Ind_FC{code}_{n}_xlsx.zip`):

| Tipo | Foglio | Descrizione | Righe/anno |
|---|---|---|---|
| IND | Indicatori | Nome, descrizione, tipo, funzione degli indicatori di performance | ~350 |
| DET | Determinanti | Fattori di contesto (F_*) con descrizione | ~130 |
| COD | Codici | Decodifica codici anomalia (es. COD_SPS_QUEST) | ~130 |

## Pipeline

```
preprocess.py {year} raw_input.csv
  → scarica 7 XLSX, estrae 3 fogli ciascuno, unisce in CSV

clean.sql → pass-through (normalizza)

mart.sql → pass-through (select * from clean_input)
```

## Anni

2015, 2016, 2017, 2018, 2019, 2021, 2022 — ogni anno produce il suo mart.
(2020 assente: solo FSC, nessun indicatore pubblicato.)
Il candidate principale referenzia il mart con `{root}/data/mart/opencivitas_glossario/{year}/mart_metadati.parquet`.
