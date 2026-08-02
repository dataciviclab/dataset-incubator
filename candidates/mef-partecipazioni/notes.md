## Note tecniche

### Encoding e parsing
- File: CSV con delimitatore `;`, encoding `latin-1`
- Header: riga 1, colonne con spazi e caratteri speciali
- 93 colonne totali per anno — schema stabile a 84 colonne comuni

### Clean.sql — scelte
- 84 colonne selezionate (di 93 totali per anno) — solo colonne comuni a tutti gli anni
- 9 colonne anno-specifiche escluse: Fatturato N, Risultato d'esercizio N, Partecipata bilancio N approvato
- Nessun filtro WHERE — raw faithful, nessuna riga esclusa
- importo_impegnato_servizio_5 è castato VARCHAR (vs BIGINT per 1-4) per anomalia dati: il campo contiene stringhe non numeriche in alcuni anni

### Mart.sql — scelte
- Aggregazione: count partecipazioni, distinct amministrazioni, distinct partecipate
- Raggruppamento: regione, provincia, comune, categoria amministrazione
- Metriche: % perimetro TUSP, % perimetro revisione periodica

### Schema variability

Il portale MEF pubblica dati con schema che varia per anno — le colonne con l'anno nel nome (es. `Fatturato 2021`, `Risultato d'esercizio 2023`) cambiano a seconda dell'anno di rilevazione. Per garantire uno schema clean costante, la clean.sql seleziona solo le 84 colonne presenti in tutti gli anni disponibili.

Anni verificati: 2020, 2021, 2022, 2023. Tutti gli anni con URL dedicato.

## Caveat analitici

- Dato dichiarativo: copertura dipende dall'adempimento
- Serie storica: 4 anni (2020-2023)
## 2026-08-02 — standard v1, mart serie

### Fix clean.sql
- `quota_soggetto_privato`: era `trim(...)` su colonna DOUBLE sniffata da DuckDB
  (percentuali con virgola es. "48,85") → BinderError `trim(DOUBLE)`.
  Corretto con `try_cast(... as double)`.

### Mart — sostituita mart_comuni (granularità comune, mai pubblicata)
- `mart_trend_anno` (multi-year): partecipazioni/amministrazioni/partecipate per
  anno, pct TUSP, delta, variazione %
- `mart_top_amministrazioni`: per amministrazione-anno: partecipazioni,
  partecipate distinte, settore/macrocategoria/categoria, regione
- `mart_sintesi_regione`: per (anno, regione, categoria): partecipazioni,
  amministrazioni distinte, pct TUSP e revisione

### Numeri chiave (2023)
- Amministrazioni in calo (8869→8360) ma partecipazioni in crescita
  (51983→53656) → concentrazione crescente
- Top amministrazioni 2023: Valle d'Aosta (181), CNR (154), Napoli Federico II (124)
- Lombardia comuni: 8.295 partecipazioni (1.429 amministrazioni)
- pct perimetro TUSP stabile ~99%

### Standard v1
- required_columns completo (85 output, mancavano 25 tra cui anno e metriche
  finanziarie) → validation_rules_coverage 100%
- primary_key [anno, amministrazione_codice_fiscale, partecipata_codice_fiscale]
  (0 duplicati, 0 null verificati)
- min_rows, table_rules con PK dai GROUP BY

### 2026-08-02 — review fix: migrazione macro standard
- clean.sql: trim/try_cast → normalize_string (58x), cast_bigint (23x),
  cast_double (3x), cast_int (1x) — macro standard toolkit
- Verificato 0 stringhe vuote nei dati: normalize_string (TRIM+NULLIF)
  identico a trim() → nessun cambio comportamento
- Run passed 4 anni, readiness 8/8, dati identici (0% drop)
