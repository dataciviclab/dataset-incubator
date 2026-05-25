# bdap-lea

## Domanda guida

Quanto pesa la prevenzione collettiva nel consuntivo 2024 delle ASL italiane, e quanto varia questo peso tra enti e territori quando si escludono le aggregazioni Regionali?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / Modello LEA enti SSN.
Discussion: `dataciviclab` Datasets #179
Issue intake: `dataset-incubator` #113

## Perimetro

- Annualità: `2024`
- Enti operativi: `codice_ente_ssn not in ('000', '999')` — esclusi aggregati regionali (`000`) ed enti regione (`999`) che causano double-counting
- Granularità: per ente SSN e regione

Attenzione: il totale include ~€166 mld di `prestazioni_sanitarie` (transazioni inter-ente per mobilità sanitaria). Ogni prestazione è contata sia dall'ente pagante sia dall'ente erogante — è un double-counting fisiologico del dato contabile BDAP, non un bug.

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
| `importo_totale` | DOUBLE | metric | Importo totale della voce |
| *(altre 14 colonne metriche: consumi, personale, servizi, ammortamenti...)* | | | |

## Layer

- **Clean**: 20.036 righe, ~396 mld € — filtra voci TOTALE (19999,29999,39999,48888,49999) + enti `000` e `999`. 23 colonne.
- **Mart**: `mart_spesa_enti_2024` — 20.036 righe, ~396 mld € — stesso perimetro del clean, rimuove `data_aggiornamento` e `oneri_finanziari`. 21 colonne.

## Output

- `out/data/clean/bdap_lea/2024/bdap_lea_2024_clean.parquet`
- `out/data/mart/bdap_lea/2024/mart_spesa_enti_2024.parquet`

## Run

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-lea/dataset.yml
```

## Stato

`runnable` — pipeline completa.
