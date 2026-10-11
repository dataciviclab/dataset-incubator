# notes — adm-accertato-accise

## Fonte e URL

- URL live verificate 2026-10-11. Inventory SO (`adm_opendata`) ha URL drift:
  - energia elettrica: inventory `...sullenergia-elettrica.csv` → live `...sull-energia-elettrica.csv`
  - gas: usare URL live con doppia L in `dell-accisa` come da landing page
- Landing page gas dichiara "12 byte" ma il file è ~12KB: metadato non affidabile per size
- Frequenza annuale; ultima modifica catalogo 2026-09-11

## Parsing

- Delimiter `;`, encoding UTF-8, header presente
- `clean.read.columns` forza **VARCHAR** su tutte le colonne raw
- `ACCERTATO`: `normalize_italian_number` (decimale `,`, interi senza virgola)
- `CODICE CAPITOLO`: cast auto DOUBLE mangiava la forma (`1.410` → `1.41`);
  in clean si normalizza `replace('.', '')` → BIGINT (`1410` sia per `1.410` sia per `1410`)
- Colonne raw con spazi (`CODICE CAPITOLO`, `DIREZIONE REGIONALE`, …) — quote in SQL

## Copertura diseguale

- Solo `prodotti_energetici` arriva a 2024 nel CSV attuale
- Gli altri settori 2022–2023: righe 2024 assenti non sono errore di pipeline
- `years: [2024]` = anno di run/snapshot (file full-series); `time_coverage` 2022–2024

## Primary key clean

- PK: `anno, settore, regione, codice_capitolo, codice_articolo` (capitolo normalizzato senza punti)
- Possono coesistere più capitoli per regione/stesso anno (es. Lombardia)

## Limite semantico del dato

- L'**accertato** è imputato ai soggetti/depositi ADM per direzione regionale,
  non al consumo finale locale: picchi in Lazio o crolli in regioni piccole
  sono spesso effetti di domicilio fiscale/sedi, non di domanda territoriale

## Mart

- `mart_accertato_regione_anno`: regione × anno × settore + `area` (nord/centro_sud),
  `quota_pct_naz`, `rank_settore`
- `mart_sintesi_area`: area × anno × settore
- `mart_trend_regioni`: primo/ultimo anno, delta %, spostamento rank

## Esclusi v0

- `dichiarazioni-accise` (~9 righe): too-thin, eventuale support dataset
- `altri-tributi-connessi`: solo 2022, candidato fase 2
