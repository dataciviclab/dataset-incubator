# mase_gas_consumi

Gas naturale **distribuito per provincia e settore**, annuale.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN), sezione *Gas naturale*
→ [sisen.mase.gov.it/dgsaie/bilancio-gas-naturale](https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale)
(source_id: `mase_dgsaie`)

**Domanda civica**: chi consuma il gas in Italia? Come si distribuisce tra industria,
centrali termoelettriche e reti di distribuzione, provincia per provincia?
([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro v0

- **Anno**: 2024 (primo taglio; la fonte copre 2004-2025)
- **Unità**: provincia × settore
- **Metrica**: `consumo_msmc` — milioni di Sm³ (PCS 10,57275 kWh/Sm³)
- **Settori**: `industriale`, `termoelettrico`, `reti` (distribuzione)

## Output

- `clean` — `anno, regione, provincia, settore, consumo_msmc` (formato lungo)
- `mart_consumo_provincia` — come clean + `quota_provincia_pct`
- `mart_consumo_regione` — rollup regionale + `quota_regione_pct`

## Come girare

```bash
toolkit run -c candidates/mase-gas-consumi/dataset.yml --year 2024
toolkit inspect -c candidates/mase-gas-consumi/dataset.yml -y 2024
```

## Incroci disponibili in Lab

- `mase_gas_import` — da dove arriva il gas (stesso publisher, stesso tema)
- `comuni_master` / `istat_elenco_comuni` — denominatore popolazione → consumo pro-capite
- `terna_copertura_domanda` — termoelettrico per regione (coerenza del settore)
- `ispra_emissioni_ghg` — emissioni per settore

## Limiti noti

- v0 = **un solo anno** (2024): la fonte espone un file per anno con ID non deterministico
  → il multi-anno richiede enumerazione via API CMIS (vedi `notes.md`).
- Il file contiene anche una riga "TOTALE" per regione: esclusa nel clean, il totale è
  ricalcolato nel mart (controllo di coerenza).
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione.
