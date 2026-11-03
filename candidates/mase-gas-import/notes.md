# Notes — mase_gas_import

## Fonte e accesso

- Portale: https://sisen.mase.gov.it/dgsaie/bilancio-gas-naturale (SPA React)
- API CMIS pubblica, **nessuna autenticazione**:
  - lista cartelle: `GET /dgsaie/api/v1/cmis/folders?folder={path}`
  - lista documenti: `GET /dgsaie/api/v1/cmis/documents?folder={path}` (param `folder` = **path**)
  - download: `GET /dgsaie/api/v1/cmis/documents/{id}`
- **Non esiste** un download per nome/path (testato: 404/401). Gli ID sono opachi →
  niente `{year}` in un `http_file` → serve il `script`.

## Perché `script` e non multi-source

Il layout **cambia tra le ere**:

| Era | Foglio | Struttura |
|---|---|---|
| 2002-2012 `.xls` | `Importazioni Paese Origine` | 2002-2009: **8 blocchi-anno impilati** in un file |
| 2013-2015 | `Foglio1` | un anno per file |
| 2016+ `.xlsx` | `Foglio2` | un anno per file |

Un `raw.sources[]` con N `http_file` + `mode: all` esplode sul concat (fogli e
blocchi diversi). `preprocess.py` individua le righe-titolo
(`IMPORTAZIONI DI GAS NATURALE … ANNO YYYY`) e legge da lì: titolo → `MESE` →
nomi mesi → dati, fino alla riga `Totale`. Vale per tutte le ere.

## Anomalia di unità 2013-2014

I due file hanno titolo **"Miliardi di standard metri cubi"** ma i valori sono in
**Sm³ grezzi**: RUSSIA gen-2013 = `2.462.201.248` (cioè 2,46 miliardi Sm³).
Il titolo è errato nella fonte.

Rilevazione: somma del blocco-anno `> 500.000` → riscala di `1e-6`.
Somme rilevate: 2013 = 61.966.186.694, 2014 = 55.851.968.603 → riscalate a
61.966 e 55.852 M Sm³. Il preprocess **logga** la correzione a ogni run.

> Se in futuro un file supera quella soglia per un motivo diverso, la soglia va rivista.

## Normalizzazione etichette paese

Le ere usano italiano e inglese, con varianti e refusi:

| Etichetta grezza | Canonica |
|---|---|
| Russian Federation | RUSSIA |
| Netherlands / Norway / Libya | OLANDA / NORVEGIA / LIBIA |
| QUATAR | QATAR |
| USA | U.S.A. |
| UK | REGNO UNITO |
| TRINIDAD TOBAGO | TRINIDAD |
| ALRI UE (refuso) | ALTRI UE |
| ALTRI Unione Europea / ALTRI non Unione Europea | ALTRI UE / ALTRI NON UE |
| `AUSTRIA (*)`, `PERU'` | AUSTRIA, PERU |

I marcatori di nota `(*)` e le virgolette sono rimossi. Righe `Totale`,
`FONTE:`, `(*) …` sono escluse (il totale si ricalcola nei mart).

## Controlli di coerenza

- Totali per anno confrontati con il `Totale` del file: 1990 = 30.470, 2000 = 57.447,
  2010 = 75.354, 2024 = 59.304 M Sm³ ✓
- 2021: 72.996 (dai file mensili) vs 72.728 (file annuale) → differenza nota,
  il mensile è la fonte più fine e prevale
- 3.984 righe clean; 3.660 mensili (23 anni) + 324 annuali (12 anni)

## Insidie

- Le etichette cambiano nel tempo: ogni nuovo anno va verificato
- I file hanno colonne extra oltre i 12 mesi (`Totale`, `Peso %`): ignorate
- `2012` è presente nei file *per paese* (il buco 2012 è nei file *per punto di ingresso*)
- Il 2022 ha `_rev1`: il preprocess preferisce la revisione

## Piste collegate

- `importazioni/` **per punto di ingresso** (2002-2024) → secondo asse, dataset separato
- `mase_gas_consumi` (provincia × settore) e `mase_consumi_petroliferi` (mensile)

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima della pubblicazione sull'Explorer.
