# bdap-lea

## Domanda guida

Quanto pesa la prevenzione collettiva nel consuntivo delle ASL italiane, e come si evolve nel tempo?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / Modello LEA enti SSN.
Discussion: `dataciviclab` Datasets #179
Issue intake: `dataset-incubator` #113

## Perimetro

- Annualità: `2019, 2020, 2021, 2022, 2023, 2024` (serie storica 6 anni)
- Enti operativi: `codice_ente_ssn not in ('000', '999')` — esclusi aggregati regionali (`000`) ed enti regione (`999`) che causano double-counting
- Granularità: per ente SSN e regione

Attenzione: il totale include le `prestazioni_sanitarie` (transazioni inter-ente per mobilità sanitaria). Ogni prestazione è contata sia dall'ente pagante sia dall'ente erogante — è un double-counting fisiologico del dato contabile BDAP, non un bug.

## Schema drift

La colonna `Oneri Finanziari` è presente solo in alcuni anni (2019, 2021, 2022, 2024). Gestito con `align_by_header: true` (toolkit PR #329) che allinea le righe CSV per nome colonna — se manca, viene inserito NULL.

Vedi `notes.md` per il dettaglio.

## Schema

23 colonne. Le principali:

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
| `oneri_finanziari` | DOUBLE | metric | Oneri finanziari (NULL se non disponibile nell'anno) |
| `importo_totale` | DOUBLE | metric | Importo totale della voce |
| *(altre 13 colonne metriche: consumi, personale, servizi, ammortamenti...)* | | | |

## Layer

- **Clean**: ~20.000 righe/anno, 23 colonne. Filtra voci TOTALE (19999,29999,39999,48888,49999) + enti `000` e `999`.
- **Mart**: `mart_spesa_enti` — stesso perimetro del clean, rimuove `data_aggiornamento`. 22 colonne.

## Output

- `out/data/clean/bdap_lea/{year}/bdap_lea_{year}_clean.parquet`
- `out/data/mart/bdap_lea/{year}/mart_spesa_enti.parquet`

## Run

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-lea/dataset.yml --year 2024
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-lea/dataset.yml --year 2023
# ... per anno desiderato
```

## Stato

`runnable` — pipeline completa.
