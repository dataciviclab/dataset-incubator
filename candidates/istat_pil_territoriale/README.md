# istat_pil_territoriale — PIL regionale e provinciale

**Support dataset** — ISTAT SDMX Dataflow 93_498 (DCCN_PILT)

## Fonte

ISTAT — Conti economici territoriali (PIL lato offerta)
SDMX-CSV: `https://esploradati.istat.it/SDMXWS/rest/data/93_498_DF_DCCN_PILT_1/all?format=csv`

## Copertura

| Livello | Entità | Anni |
|---|---|---|
| nazionale | 1 (Italia) | 1995–2024 |
| macro-aree | 9 (Nord-ovest, Mezzogiorno, …) | 1995–2023 |
| regioni | 21 (20 + PA Bolzano/Trento) | 1995–2023 |
| province | 107 | 1995–2023 |

**Nota**: 2024 è disponibile solo per il nazionale. Per regioni e province l'ultimo anno è 2023.

## Metriche

- `pil_mln_eu` — PIL ai prezzi di mercato (milioni € correnti)
- `va_mln_eu` — Valore Aggiunto (milioni € correnti)
- `imposte_nette_mln_eu` — Imposte nette sui prodotti (milioni € correnti)

## Colonne output

**Clean** (10.167 righe): `territorio_codice`, `territorio_nome`, `livello`, `tipo_dato_codice`, `valutazione_codice`, `anno`, `valore_mln_eu`

**Mart** (3.360 righe): `territorio_codice`, `territorio_nome`, `livello`, `anno`, `pil_mln_eu`, `va_mln_eu`, `imposte_nette_mln_eu`

## Join keys

- `territorio_codice` — codici ISTAT/NUTS (ITC1=Piemonte, ITC11=Torino, …)
- `anno` — anno di riferimento

## Uso previsto

Support dataset per normalizzare e contestualizzare analisi esistenti:
- PIL pro-capite (join con `popolazione_istat_comunale`)
- Incidenza spesa pubblica su PIL (Consip, BDAP, pensioni)
- Contesto macroeconomico per analisi territoriali

## Run

✅ `toolkit run full --years 2024` passato
raw✅ clean✅ (10.167 righe, 7 colonne) mart✅ (3.360 righe)
readiness: ready (5/5)
