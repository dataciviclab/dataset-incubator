# mase_gas_consumi

Gas naturale **distribuito per provincia e settore**, serie storica.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN), sezione *Gas naturale*
→ [sisen.mase.gov.it/dgsaie/bilancio-gas-naturale](https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale)
(source_id: `mase_dgsaie`)

**Domanda civica**: chi consuma il gas in Italia, e come è cambiato nel tempo tra
industria, centrali elettriche e riscaldamento?
([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro

- **Periodo**: **2004-2025**
- **Unità**: provincia × settore × anno (111 province nel periodo)
- **Metrica**: `consumo_msmc` — milioni di Sm³ (PCS 10,57275 kWh/Sm³)
- **Settori**: `industriale`, `termoelettrico`, `reti` (distribuzione)

## Output

- `clean` — `anno, regione, provincia, settore, consumo_msmc`
- `mart_consumo_provincia` — come clean + `quota_pct` sul totale provinciale
- `mart_consumo_regione` — rollup regionale + `quota_pct`

## Come girare

```bash
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run -c candidates/mase-gas-consumi/dataset.yml --year 2025
toolkit inspect -c candidates/mase-gas-consumi/dataset.yml -y 2025
```

`preprocess.py` scarica i 22 file annuali (2004-2025) e risolve la regione
(nella fonte è in fondo al blocco, sulla riga `TOTALE`). `2025` è **nominale**.

## Cosa dice la serie

| Settore | 2004 | 2014 | 2024 |
|---|---|---|---|
| industriale | 17.253 | 13.581 | **12.006** |
| termoelettrico | 26.556 | 17.902 | **20.944** |
| reti | 35.231 | 29.451 | **27.881** |

L'industria ha perso ~30% in 20 anni; il termoelettrico scende fino al 2014 e
risale dal 2021 (il gas torna a fare elettricità).

## Incroci disponibili in Lab

- `mase_gas_import` — da dove arriva il gas (stesso publisher)
- `comuni_master` / `popolazione_istat_comunale` — denominatore → consumo pro-capite
- `terna_copertura_domanda` — termoelettrico per regione (coerenza del settore)
- `ispra_emissioni_ghg` — emissioni per settore

## Limiti noti

- Il numero di province varia nel tempo (102 → 104 → 106 → 110): riflette le
  riorganizzazioni amministrative, non un buco nei dati
- La fonte contiene una riga `TOTALE` per regione: esclusa, il totale è ricalcolato
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione
