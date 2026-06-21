# unified-comuni

Dataset composito che unisce popolazione, redditi, rifiuti e Fondo di
Solidarietà Comunale per comune italiano. Ogni riga = comune × anno.

Legge i parquet clean già pubblicati su GCS via **S3 glob patterns**
(nessuna lista file da mantenere). Hub centrale: `comuni_master`.

## Fonti incluse

| Dominio | Dataset | Periodo | Metodo |
|---------|---------|:-------:|--------|
| Hub | `comuni_master` | 2026 | raw `http_file` |
| Popolazione | `popolazione_istat_comunale` | 2019–2025 | S3 glob |
| IRPEF | `irpef_comunale` | 2019–2024 | S3 glob |
| Rifiuti | `ispra_ru_base` | 2020–2024 | S3 glob |
| FSC | `opencivitas_fsc_2025_rso` | 2025 | S3 |

## Schema

```
codice_istat, anno
denominazione, sigla_provincia, regione
popolazione_residente
contribuenti, reddito_imponibile_eur
ru_tot (tonnellate), rd_pct
dotazione_finale_fsc
```

## Join Map

Tutte le chiavi in `registry/join_map.yaml`. Hub: `codice_istat` (6 cifre).

## Run

```bash
toolkit run full --config candidates/unified-comuni/dataset.yml --years 2026
```

## Mantenimento

Quando un nuovo anno viene pubblicato per una fonte (es. IRPEF 2025),
basta che il file sia su GCS — il candidate va ri-runato e il nuovo anno
viene preso automaticamente dall'S3 glob. Nessuna modifica al codice.
