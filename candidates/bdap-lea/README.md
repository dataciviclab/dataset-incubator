# bdap-lea

## Domanda guida

Quanto pesa la prevenzione collettiva nel consuntivo 2024 delle ASL italiane, e quanto varia questo peso tra enti e territori quando si escludono le aggregazioni Regionali?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / Modello LEA enti SSN.
Discussion: `dataciviclab` Datasets #179
Issue intake: `dataset-incubator` #113

## Perimetro

- Annualità: `2019, 2020, 2021, 2022, 2023, 2024` (serie storica)
- Enti operativi: `codice_ente_ssn not in ('000', '999')` — esclusi aggregati regionali (`000`) ed enti regione (`999`) che causano double-counting
- Granularità: per ente SSN, regione e anno

Attenzione: il totale include ~€166 mld di `prestazioni_sanitarie` (transazioni inter-ente per mobilità sanitaria). Ogni prestazione è contata sia dall'ente pagante sia dall'ente erogante — è un double-counting fisiologico del dato contabile BDAP, non un bug.

### Schema drift: colonna "Oneri Finanziari"

La colonna "Oneri Finanziari" è presente nei CSV BDAP solo per alcuni anni della serie:

| Anno | Oneri Finanziari |
|:----:|:----------------:|
| 2019 | ✅ |
| 2020 | ❌ |
| 2021 | ✅ |
| 2022 | ✅ |
| 2023 | ❌ |
| 2024 | ✅ |

Gestito con `align_by_header: true` nel `clean.read` (toolkit ≥ v1.25.0): il reader allinea le righe per nome colonna, inserendo `NULL` per le annualità senza il campo.

## Schema

23 colonne (22 per 2020 e 2023, con `oneri_finanziari = NULL`). Le principali:

| Colonna | Tipo | Ruolo | Descrizione |
|---|---|---|---|
| `anno_riferimento` | INTEGER | dimension | Anno di riferimento |
| `codice_regione` | VARCHAR | dimension | Codice regione |
| `descrizione_regione` | VARCHAR | dimension | Denominazione regione |
| `codice_ente_ssn` | VARCHAR | dimension | Codice ente SSN |
| `codice_ente_bdap` | BIGINT | dimension | Codice BDAP ente |
| `descrizione_ente` | VARCHAR | dimension | Denominazione ente |
| `codice_voce_contabile` | VARCHAR | dimension | Codice voce contabile |
| `descrizione_voce_contabile` | VARCHAR | dimension | Descrizione voce contabile |
| `oneri_finanziari` | DOUBLE | metric | Oneri finanziari (NULL per 2020, 2023) |
| `importo_totale` | DOUBLE | metric | Importo totale della voce |
| *(altre 13 colonne metriche: consumi, personale, servizi, ammortamenti...)* | | | |

## Layer

- **Clean**: ~20.000 righe/anno × 6 anni — filtra voci TOTALE (19999,29999,39999,48888,49999) + enti `000` e `999`. 23 colonne.
- **Mart**: stesso perimetro del clean, rimuove `data_aggiornamento` e `oneri_finanziari`. 21 colonne.

## Output

- `out/data/clean/bdap_lea/{year}/bdap_lea_{year}_clean.parquet`
- `out/data/mart/bdap_lea/{year}/mart_spesa_enti.parquet`

## Run

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-lea/dataset.yml --year 2024
# oppure tutti gli anni:
for y in 2019 2020 2021 2022 2023 2024; do
  python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-lea/dataset.yml --year $y
done
```

Richiede toolkit ≥ v1.25.0 (flag `align_by_header`).

## Stato

`runnable` — pipeline completa su 6 annualità.
