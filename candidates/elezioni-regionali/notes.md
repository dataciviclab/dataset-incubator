# Note tecniche — elezioni-regionali

## Struttura

```
candidates/elezioni-regionali/
├── dataset.yml        # script source multi-anno
├── preprocess.py      # download, unzip, normalizza
├── sql/
│   ├── clean.sql      # schema unificato 12 colonne
│   └── mart.sql       # aggregazione lista × comune
├── README.md
└── notes.md
```

## Perimetro

6 anni, 9 tornate, esclusa 2020-09-20 (XLSX).

## Mappa fonti

| Anno | URL | Formato |
|---|---|---|
| 2018 | ZIP `regionali-20180304.zip` | 2 TXT (scrutini + preferenze) |
| 2019a | ZIP `regionali-20190210.zip` | 2 TXT |
| 2019b | ZIP `regionali-20190324.zip` | 2 TXT |
| 2019c | ZIP `regionali-20190526.zip` | 2 TXT |
| 2019d | ZIP `regionali-20191027.zip` | 2 TXT |
| 2020 | ZIP `regionali-20200126.zip` | 2 TXT |
| 2021 | ZIP `regionali-20211003.zip` | 2 TXT (nomi file diversi) |
| 2023 | CSV diretto catalogoagid | 1 CSV |
| 2024 | ZIP `regionali-20240609.zip` | 1 CSV (combinato) |

## Variazioni schema raw tra anni

Il `preprocess.py` normalizza tutte queste differenze:

### Nomi colonna
| Concetto | 2018-2020 | 2021 | 2023 | 2024 |
|---|---|---|---|---|
| Regione | `REGIONE` | `REGIONE` | `REGIONE` | `REG` |
| Circoscrizione | `CIRCOSCRIZIONE` | `CIRCOSCRIZIONE` | `CIRCOSCRIZIONE` | `CIRC` |
| Provincia | `PROVINCIA` | `provincia` (lower!) | `PROVINCIA` | `PROV` |
| Elettori | `ELETTORI` | `ELETTORI` | `ELETTORITOT` | `ELETTORITOT` |
| Voti candidato | `VOTI_CANDIDATO` | `VOTI_CANDIDATO` | `VOTICAND` | `VOTICANDIDATO` |
| Lista | `LISTA` | `LISTA` | `DESCRLISTA` | `DESCRLISTA` |

### Formato numeri
- 2018-2021: comma decimal (`5849,00`) — il preprocess normalizza a interi
- 2023-2024: interi diretti

### Encoding
- 2019-05-26 (Piemonte): ISO-8859-1 (lettere accentate in nomi/luoghi)
- Tutti gli altri: ASCII / UTF-8
- Preprocess: tentativo UTF-8 → latin-1 → cp1252

### Nomi file dentro ZIP
| Periodo | File scrutini | File preferenze |
|---|---|---|
| 2018-2020, 2023 | `regionali-YYYYMMDD.txt` / `.csv` | `Preferenze_*.txt` / `.csv` |
| 2021 | `scrutini-YYYYMMDD.txt` | `CandidatiLista-Preferenze_*.txt` |
| 2024 | `regionali-YYYYMMDD.csv` (unico) | N/A |

## Note implementative

### Perché preprocess invece di http_file diretto
- Ogni anno ha URL diverso (non template {year} semplice)
- ZIP con 2 file di cui serve solo 1 (scrutini)
- Nomi colonna e formati numerici variano per anno
- Encoding misto (utf-8 / latin-1)

### TOOLKIT_ALLOW_SCRIPT_SOURCE
Il source type `script` è disabilitato di default per sicurezza.
Va attivato con `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` nell'ambiente di run.

### Esclusioni
- **2020-09-20**: file XLSX. Il toolkit non gestisce Excel via ZIP extractor.
  Soluzione futura: estrarre XLSX manualmente o estendere toolkit.
- **2014 e precedenti**: schema diverso (no circoscrizione, formato intero).
  Estendere in futuro.
- **File preferenze**: ogni ZIP ha un secondo file con i voti di preferenza
  ai singoli consiglieri. Non incluso nel perimetro iniziale.

## Verifica

```bash
cd dataset-incubator
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run full \
  --config candidates/elezioni-regionali/dataset.yml \
  --years 2018,2019,2020,2021,2023,2024
```

## Output pipeline

| Anno | Layer | Righe | Qualità |
|---|---|---|---|
| 2018 | clean | 35.060 | 100 |
| 2019 | clean | 24.645 | 100 |
| 2020 | clean | 10.299 | 100 |
| 2021 | clean | 8.484 | 100 |
| 2023 | clean | 24.125 | 100 |
| 2024 | clean | 15.266 | 100 |

## Cross-repo

Issue: https://github.com/DataCivicLab/dataset-incubator/issues/588
Scorporata da: https://github.com/DataCivicLab/dataset-incubator/issues/523
Fonte SO: `eligendo` (radar-only)
