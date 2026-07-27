# Note tecniche — eurostat-economy

## Architettura

Compose che legge parquet puliti direttamente da GCS (repo `dataciviclab/eurostat`). Nessuna dipendenza da fonti live Eurostat.

1. **Hub**: area_nuts3 (geo NUTS) × gdp_nuts3 (anni 2000-2024) → tutte le combinazioni EU-wide
2. **4 CTE dominio**: GDP, GVA, employment, produttività
3. **LEFT JOIN** su (geo, year)
4. **WHERE** elimina righe senza alcun dato

## Dataset sorgente su GCS

```
https://storage.googleapis.com/dataciviclab-clean/eurostat/{slug}/{slug}_2026_clean.parquet
```

## Qualità (run 2026-07-26)

| Metrica | Valore |
|---|---|
| Righe clean EU | 41.709 |
| Colonne | 26 |
| GDP per capita non-NULL | 97.2% |
| GVA totale non-NULL | 100% |
| Employment non-NULL | 90.5% |
| Produttività non-NULL | 90.5% |
| IT NUTS3 coverage | 107/107 province (tutti gli anni) |

## Filtro anti-NULL

La SELECT finale include `WHERE gdp_per_capita IS NOT NULL OR gva_total_million IS NOT NULL OR employment_thousands IS NOT NULL` per eliminare righe (geo × year) senza dati economici.
