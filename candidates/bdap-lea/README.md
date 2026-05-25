# bdap-lea

## Domanda guida

Quanto pesa la prevenzione collettiva nel consuntivo 2024 delle ASL italiane, e quanto varia questo peso tra enti e territori quando si escludono le aggregazioni Regionali?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / Modello LEA enti SSN.
Discussion: `dataciviclab` Datasets #179
Issue intake: `dataset-incubator` #113

## Perimetro

- Annualità: `2024`
- Enti operativi: `codice_ente_ssn != '000'` (esclusi aggregati Regionali)
- Granularità: per ente SSN e regione

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno_riferimento` | INTEGER | Anno di riferimento |
| `codice_regione` | VARCHAR | Codice regione |
| `denominazione_regione` | VARCHAR | Denominazione regione |
| `codice_ente_ssn` | VARCHAR | Codice ente SSN |
| `denominazione_ente` | VARCHAR | Denominazione ente |
| `codice_modello_lea` | VARCHAR | Codice modello LEA |
| `descrizione_modello_lea` | VARCHAR | Descrizione modello LEA |
| `importo_totale` | DOUBLE | Importo totale |
| `flag_aggregazione` | VARCHAR | Flag aggregazione |

## Layer

- **Clean**: 23.595 righe — filtra voci di totale contabile (codici 19999, 29999, 39999, 48888, 49999) che duplicavano gli importi di dettaglio. SUM importo_totale: 748 mld €
- **Mart**: `mart_spesa_enti_2024` — 22.180 righe — filtro `codice_ente_ssn != '000'` + eredita filtro voci totali dal clean. SUM importo_totale: 738 mld €

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
