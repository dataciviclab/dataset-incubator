# adm-accertato-accise

## Domanda civica

Quanto si accerta di accisa per regione e settore merceologico, e come si
distribuisce il carico fiscale indiretto tra territori? La fiscalità
energetica e alcolica ha effetti diversi per area: leggere l'accertato ADM
per regione × anno × settore serve a osservare concentrazione geografica
e trend (es. shock energetico 2022–2023) senza join esterne.

## Dataset / fonte

Agenzia delle Dogane e dei Monopoli (ADM) — open data su dati.gov.it
(CC BY 4.0), catalogo `adm_opendata`. Quattro CSV con schema unico:

| File | Settore inject | Copertura osservata |
|---|---|---|
| accertato prodotti energetici | `prodotti_energetici` | 2022–2024 |
| accertato gas naturale | `gas_naturale` | 2022–2024 |
| accertato energia elettrica | `energia_elettrica` | 2022–2024 |
| accertato prodotti alcolici | `prodotti_alcolici` | 2022–2024 |

Grato riga: regione (o DR ADM) × anno × capitolo/articolo × tipo tributo.
Metrica: `ACCERTATO` (euro, decimale italiano).

## Perché vale la pena

- Fonte ufficiale, già in inventory SO (score 9–10), tutte le URL live verificate 2026-10-11
- Schema stabilità e join-free: 8 colonne + inject `settore`
- Copertura multi-anno utile per trend post-crisi energetica
- Base per mart territoriale confrontabile tra settori

## Output minimo atteso

- Clean unificato multi-settore con parsing numerico italiano
- `mart_accertato_regione_anno`: regione × anno × settore, quota e rank
- `mart_sintesi_area`: nord / centro-sud × anno × settore
- `mart_trend_regioni`: delta e spostamento rank primo→ultimo anno

## Criterio di promozione

- Readiness `ready` sul run v0
- Mart con 20 regioni × settori × anni disponibili, valori plausibili (ordini di grandezza ADM)
- Domanda civica ancora leggibile senza arricchimenti obbligatori

## Stato / prossimo passo

- Issue: [#865](https://github.com/dataciviclab/dataset-incubator/issues/865)
- Stato: candidate v0 — `toolkit run` 2024 `ready` (8/8), 3 mart
- Prossimo: review PR, poi eventuale notebook/analisi e Discussion Domanda
