# Note tecniche — eurostat-territory

## Architettura

Compose che legge parquet puliti direttamente da GCS.

1. **Hub**: area_nuts3 × gdp_nuts3 (anni 2000-2024)
2. **4 CTE dominio**: superficie, turismo, criminalità, incidenti
3. **LEFT JOIN** su (geo, year)
4. **WHERE** elimina righe senza alcun dato

## Qualità (run 2026-07-26)

| Metrica | Valore |
|---|---|
| Righe clean EU | 30.495 |
| Colonne | 11 |
| Area non-NULL | 61.8% |
| Pernottamenti non-NULL | 47.3% |
| Reati non-NULL | 73.7% |
| Incidenti non-NULL | 61.3% |
| IT NUTS3 coverage | 107/107 province |

## Copertura parziale

I dataset territoriali Eurostat hanno copertura non uniforme:
- **area_km2**: disponibile da 2013 (prima solo stime), per questo 38% NULL su periodo 2000-2024
- **tourism**: paesi extra-UE spesso non coperti, e regioni non turistiche hanno dati zero/non disponibili
- **crime**: non tutti i paesi EU trasmettono dati criminalità a Eurostat
- **road accidents**: coverage simile a crime, paesi EU mediterranei hanno dati più recenti

I NULL sono gestiti dal LEFT JOIN — indicano "dato non disponibile per questa regione/anno", non un errore.
