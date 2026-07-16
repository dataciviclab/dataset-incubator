# opencivitas-indicatori

**Dataset EAV multi-ambito degli indicatori di performance dei comuni italiani.**

Fonte: [OpenCivitas](https://www.opencivitas.it/) (ANCI/Sogei) — sitemap XML.

## Schema

Formato EAV (Entity-Attribute-Value) arricchito con geografia e descrizioni.

| Colonna | Tipo | Note |
|---|---|---|
| `username` | VARCHAR | Codice ente Sogei (chiave) |
| `anno` | INTEGER | 2018, 2019, 2021, 2022 |
| `ambito` | VARCHAR | Servizio: `amministrazione`, `istruzione`, `polizia_locale`, `rifiuti`, `sociale_asili_nido`, `viabilita_territorio`, `servizi_totali` |
| `indicatore` | VARCHAR | Nome indicatore (es. `COPERTURA_NID_NEW`) |
| `valore_num` | DOUBLE | Valore numerico |
| `descrizione_indicatore` | VARCHAR | Descrizione leggibile (da glossario) |
| `tipo_indicatore` | VARCHAR | IND/DET/COD |
| `denominazione` | VARCHAR | Nome comune |
| `provincia` | VARCHAR | Codice ISTAT provincia (3 cifre) |
| `regione` | VARCHAR | Nome regione |
| `codice_istat` | VARCHAR | Codice ISTAT comune (6 cifre) |

## Copertura

- **7 anni**: 2015, 2016, 2017, 2018, 2019, 2021, 2022 (2020 assente)
- **7 ambiti** tematici per anno
- **~280 indicatori** per anno (media)
- **19,4M righe** clean (7 anni)
- **~90% comuni italiani** coperti (RSO)

## Support dataset

| Support | Ruolo |
|---|---|
| `opencivitas_fsc_enti_rso` | Anagrafica enti (username → denominazione/regione) |
| `opencivitas_glossario` | Dizionario indicatori (IND), determinanti (DET), codici (COD) |
| `comuni_master` | Golden record comuni (codice ISTAT, catastale) |

## Pipeline

1. `preprocess.py {year} raw_input.csv` — scarica 7 ZIP, estrae CSV, unisce in EAV
2. `sql/clean.sql` — normalizza valori, join enti + glossario
3. `sql/mart.sql` — arricchisce con comuni_master

## Qualità

- Drop 10-12%: valori testuali attesi (es. motivi di non valutabilità)
- Enti riconosciuti: 99%+
- Metadati trovati: ~100%
