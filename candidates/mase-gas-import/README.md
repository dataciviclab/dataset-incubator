# mase_gas_import

Import di gas naturale in Italia **per paese di origine**, mensile.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN), sezione *Gas naturale*
→ [sisen.mase.gov.it/dgsaie/bilancio-gas-naturale](https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale)
(source_id: `mase_dgsaie`)

**Domanda civica**: da dove arriva il gas che consumiamo e quanto lo paghiamo?
([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro v0

- **Anno**: 2024 (primo taglio; la fonte copre 2002-2024)
- **Unità**: paese di origine × mese
- **Metrica**: `import_msmc` — milioni di Sm³ (PCS 10,57275 kWh/Sm³)

## Output

- `clean` — `anno, mese, paese_origine, import_msmc`
- `mart_import_paese_mensile` — come clean + `quota_pct` sul totale mensile

## Come girare

```bash
toolkit run -c candidates/mase-gas-import/dataset.yml --year 2024
toolkit inspect -c candidates/mase-gas-import/dataset.yml -y 2024
```

## Incroci disponibili in Lab

- `gme_pun_storico.psv_eur_smc` — prezzo gas ingrosso PSV (mensile, 2020+)
- `eurostat_nrg_bal_c` — bilancio energetico Eurostat (IMP/GIC, 1990+)
- `terna_copertura_domanda` — termoelettrico per regione (gas → elettricità)
- `ispra_emissioni_ghg` — emissioni per settore

## Limiti noti

- v0 = **un solo anno** (2024): la fonte espone un documento per anno con ID non
  deterministico → il multi-anno richiede enumerazione via API CMIS (vedi `notes.md`).
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione.
