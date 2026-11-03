# mase_gas_import

Import di gas naturale in Italia **per paese di origine**, serie storica.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN), sezione *Gas naturale*
→ [sisen.mase.gov.it/dgsaie/bilancio-gas-naturale](https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale)
(source_id: `mase_dgsaie`)

**Domanda civica**: da dove arriva il gas che consumiamo, e come è cambiata la
dipendenza dai fornitori? ([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro

- **Periodo**: **1990-2024** (annuale 1990-2001, mensile 2002-2024)
- **Unità**: paese di origine × anno (× mese dal 2002)
- **Metrica**: `import_msmc` — milioni di Sm³ (PCS 10,57275 kWh/Sm³)
- **34 paesi**, incluse le voci aggregate (`ALTRI UE`, `ALTRI NON UE`, `NON SPECIFICATO`)

## Output

- `clean` — `anno, mese, granularita, paese_origine, import_msmc`
  (`mese` NULL sugli anni annuali; `granularita` ∈ `mensile` | `annuale`)
- `mart_import_paese` — granularità nativa + `quota_pct` sul periodo
- `mart_import_annuale` — una riga per anno × paese + `quota_pct` (la tabella per
  leggere l'evoluzione del mix dal 1990)

## Come girare

```bash
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run -c candidates/mase-gas-import/dataset.yml --year 2024
toolkit inspect -c candidates/mase-gas-import/dataset.yml -y 2024
```

`preprocess.py` enumera la cartella CMIS e scarica **tutti** i file (annuale
1990-2021 + mensili 2002-2024) producendo un unico `raw_input.csv`. L'anno
`2024` è **nominale** (rilascio più recente), non un filtro.

## Il numero che racconta la storia

Quota della Russia sul totale import: **45,9% (1990) → 47,1% (2019) → 4,1% (2024)**.
Sostituita da Azerbaigian (0% → 17,4%, via TAP), Qatar e USA (GNL), Norvegia.

## Incroci disponibili in Lab

- `gme_pun_storico.psv_eur_smc` — prezzo gas all'ingrosso (mensile, 2020+)
- `eurostat_nrg_bal_c` — bilancio energetico Eurostat (IMP/GIC, 1990+)
- `mase_gas_consumi` — dove finisce il gas (provincia × settore)
- `comtrade_bilateral` / `resource_dependency_compose` — dipendenza commerciale

## Limiti noti

- 1990-2001 è **annuale**: il mensile esiste solo dal 2002
- I file **2013-2014 sono in Sm³ grezzi** nonostante il titolo dica "Miliardi":
  `preprocess.py` li riscala di 1e-6 (vedi `notes.md`)
- Le etichette paese cambiano lingua tra le ere: normalizzate nel preprocess
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione
