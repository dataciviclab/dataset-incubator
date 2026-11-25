# istat-pil-territoriale — PIL regionale e provinciale

**Support dataset** — ISTAT SDMX Dataflow 93_498 (DCCN_PILT)

## Fonte

ISTAT — Conti economici territoriali (PIL lato offerta)
SDMX-CSV: `https://esploradati.istat.it/SDMXWS/rest/data/93_498_DF_DCCN_PILT_1/all?format=csv`

## Copertura

| Livello | Entità | Anni reali |
|---|---|---|
| nazionale | 1 (Italia) | 1995–2023 |
| macro-aree | 9 (Nord-ovest, Mezzogiorno, …) | 1995–2023 |
| regioni | 21 (20 + PA Bolzano/Trento) | 1995–2023 |
| province | 107 | 2000–2022 |

**Nota**: il campo `years: [2024]` in `dataset.yml` è l'anno del run toolkit, non la copertura dati. ISTAT non espone ancora regioni/province al 2024 in questo dataflow.

## Metriche

- `B1GQ_B_W2_S1` — PIL ai prezzi di mercato (milioni € correnti)
- `B1G_B_W2_S1` — Valore Aggiunto (milioni € correnti)
- `D21X31_C_W2_S1` — Imposte nette sui prodotti (milioni € correnti)

## Colonne output

**Clean** (10.167 righe): `territorio_codice`, `territorio_nome`, `livello`, `tipo_dato_codice`, `tipo_dato`, `valutazione_codice`, `valutazione`, `anno`, `valore_mln_eu`

**Mart** (3.360 righe): `territorio_codice`, `territorio_nome`, `livello`, `anno`, `pil_mln_eu`, `va_mln_eu`, `imposte_nette_mln_eu`

## Join keys

- `territorio_codice` — codici ISTAT/NUTS (ITC1=Piemonte, ITC11=Torino, …)
- `anno` — anno di riferimento

## Uso previsto

Support dataset per normalizzare e contestualizzare analisi esistenti:
- PIL pro-capite (join con `popolazione_istat_comunale`)
- Incidenza spesa pubblica su PIL (Consip, BDAP, pensioni)
- Contesto macroeconomico per analisi territoriali
- Confronto Istat province vs Eurostat NUTS3 (stessa unità, due fonti)

## Run

- Clean su GCS: presente (giu 2026), 10.167 righe
- Mart: **rigenerato 2026-10-06** da clean locale/GCS → 3.360 righe, 138 territori
- Raw SDMX: **non affidabile** — rate limit ISTAT (~5 req/min) e redirect-loop frequenti

```bash
# Solo mart (nessuna chiamata ISTAT) — consigliato se raw fallisce
toolkit run mart -c dataset.yml -y 2024

# Full (solo se SDMX è stabile e rispetti il rate limit)
toolkit run full -c dataset.yml -y 2024
```

## Copertura metriche nel mart

| livello | righe |
|---|---|
| provincia | 2.461 |
| regione | 609 |
| macro_area | 261 |
| nazionale | 29 |

## Copertura metriche nel mart

| livello | righe |
|---|---|
| provincia | 2.461 |
| regione | 609 |
| macro_area | 261 |
| nazionale | 29 |

## Licenza

- **Dati**: CC BY 4.0 (Istat)
- **Codice**: MIT
