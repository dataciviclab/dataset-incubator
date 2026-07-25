# ispra-ru-base

## Fonte

[Catasto Rifiuti ISPRA](https://www.catasto-rifiuti.isprambiente.it/) — sezione "Dettaglio comunale".
CSV storico disponibile per anno dal 2010. Ogni riga = un comune per anno.

## Schema

10 colonne: anno, codice ISTAT, regione, provincia, comune, popolazione,
totale RU (t), totale RD (t), percentuale RD.

## Limiti / caveat

- `percentuale_rd` è già calcolata da ISPRA (RD / RU * 100). Il dato è comunale.
- Dato riferito a = "Comune" per tutti i record (il filtro è nel clean.sql).
- Codice ISTAT pulito da caratteri di controllo (chr(9)).
- Popolazione: fonte ISPRA, non ISTAT. Può differire da dati anagrafici ufficiali.
- Valori null in popolazione, tonnellate o RD% vengono esclusi dal mart.

## Mart

5 tabelle:
- `mart_comuni` — dettaglio comunale con kg/abitante calcolati
- `mart_rd_provincia` — RD% medio pesato per provincia
- `mart_ranking_comuni` — ranking comuni per RD% con classe di popolazione
- `mart_trend_regionale` — trend 2010-2024 con CAGR e pendenza
- `mart_kg_procapite` — kg RU e RD pro-capite per provincia

## Stato
- Dati raw: download diretto HTTP CSV
- Anni: 2010-2024 completi
- Clean: macro toolkit (normalize_string, cast_bigint, normalize_italian_number)
- Pubblicato su data-explorer: S (`rifiuti-urbani`)
