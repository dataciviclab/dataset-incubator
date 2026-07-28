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

## Mart (rifattorizzati 2026-07-27)

3 tabelle (da 5):
- `mart_comuni` — arricchimento kg/abitante + benchmark RD% (media nazionale/regionale, percentile, fascia, classe demografica, rank classe). Unifica i vecchi `mart.sql`, `mart_ranking_comuni`.
- `mart_sintesi` — statistiche provinciali (RD% medio pesato, kg procapite, std, min, max). Unifica i vecchi `mart_rd_provincia`, `mart_kg_procapite`.
- `mart_trend` — trend e CAGR per provincia e regione, con segnale di tendenza. Rimpiazza `mart_trend_regionale` estendendolo a livello provinciale.

Rimosse: `mart_rd_provincia.sql`, `mart_ranking_comuni.sql`, `mart_kg_procapite.sql`, `mart_trend_regionale.sql`, `mart.sql`.

## Stato
- Dati raw: download diretto HTTP CSV
- Anni: 2010-2024 completi
- Clean: macro toolkit (normalize_string, cast_bigint, normalize_italian_number)
- Pubblicato su data-explorer: S (`rifiuti-urbani`)
