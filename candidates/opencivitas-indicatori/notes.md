# opencivitas-indicatori — Note

## Origine

Fonte: [OpenCivitas](https://www.opencivitas.it/) (ANCI/Sogei).
Dataset pubblicati come ZIP con CSV in formato EAV (USERNAME;Indicatore;Valore;Anomalia;Privacy).
Catalogo completo via sitemap XML: 271 dataset totali.

## Due ere

- **2009-2013**: formato wide (spesa storica, fabbisogni), chiave = COMUNE_CAT_COD
- **2015-2022**: formato EAV (indicatori e determinanti), chiave = USERNAME

Questo candidate copre la **seconda era**: 7 ambiti × 7 anni (2015-2022, salto 2020) in formato EAV.

## Pipeline

```
preprocess.py {year} raw_input.csv
  → scarica 7 ZIP, estrae CSV, unisce con colonna ambito
  
clean.sql
  → normalizza username, anno, indicatore
  → converte valore (decimale , → .)
  → LEFT JOIN enti su username (denominazione, provincia, regione)
  → LEFT JOIN glossario su (codice_indicatore, anno, ambito)
  
mart.sql
  → LEFT JOIN comuni_master su (denominazione, provincia)
  → aggiunge codice_istat, codice_catastale
```

## Support dataset

| Nome | Ruolo | Note |
|---|---|---|
| `opencivitas_fsc_enti_rso` | Anagrafica enti | username → denominazione/regione |
| `opencivitas_glossario` | Dizionario | 3 fogli: IND + DET + COD |
| `comuni_master` | Golden record | codice_istat, catastale |

## Qualità

- Drop 10-12%: valori testuali attesi (descrizioni, codici anomalia)
- Enti riconosciuti: 99,8%
- Glossario coperto: ~100%
- Match ISTAT: 97,9%
- Duplicati: 0 (sulla chiave username+anno+ambito+indicatore)

## Placeholder toolkit

- `{root}` → output root (es. `.../dataset-incubator/out`)
- `{year}` → anno corrente del candidate
- `{support.*.mart}` → mart del support dataset
