# ispra-consumo-suolo

**Domanda guida:** Quali territori continuano a consumare più suolo, e quanto
pesa ancora il consumo recente rispetto allo stock già accumulato?

**Fonte:** ISPRA — Consumo di suolo, dinamiche territoriali e servizi ecosistemici
**Formato:** XLSX (foglio `Comuni_2006_2024`) — [download](https://www.isprambiente.gov.it/it/attivita/suolo-e-territorio/suolo/il-consumo-di-suolo/consumo_di_suolo_estratto_dati_2025_anni_2006_2024.xlsx)
**Licenza:** CC BY 3.0 IT
**Granularità:** comune
**Copertura:** 2006–2024, 11 periodi (2 pluriennali + 9 annuali)
**Issue di riferimento:** [#32](https://github.com/dataciviclab/dataset-incubator/issues/32), [#70](https://github.com/dataciviclab/dataset-incubator/issues/70)

## Formato: long (wide → long dal 2026-06-28)

Il dataset è in **formato long**: una riga per comune × periodo (11 periodi).
Lo stock di suolo consumato per gli anni precedenti al 2024 è **ricostruito**
per differenza cumulativa dagli incrementi netti.

### Periodi

| Periodo | Anno fine | Tipo |
|---|---|---|
| 2006-2012 | 2012 | Pluriennale |
| 2012-2015 | 2015 | Pluriennale |
| 2015-2016 | 2016 | Annuale |
| 2016-2017 | 2017 | Annuale |
| … | … | … |
| 2023-2024 | 2024 | Annuale |

### Schema clean (11 colonne)

```
pro_com           VARCHAR   — Codice ISTAT comune
comune            VARCHAR   — Nome comune
provincia         VARCHAR   — Nome provincia
regione           VARCHAR   — Nome regione
periodo           VARCHAR   — Periodo (es. "2015-2016")
anno              INTEGER   — Anno finale del periodo
incremento_netto_ha  DOUBLE — Incremento netto nel periodo (ha)
incremento_lordo_ha  DOUBLE — Incremento lordo nel periodo (ha)
ripristino_ha     DOUBLE   — Aree ripristinate nel periodo (ha)
stock_ha          DOUBLE   — Stock suolo consumato a fine periodo (ha)
stock_pct         DOUBLE   — Stock suolo consumato % a fine periodo
```

## Mart disponibili

| Mart | Descrizione | Righe |
|---|---|---|
| `mart_comuni` | Dati clean pass-through | ~86.856 |
| `mart_trend_nazionale` | Trend annuale Italia (2016–2024) | ~9 |
| `mart_trend_regionale` | Trend annuale per regione | ~180 |
| `mart_trend_provinciale` | Trend annuale per provincia | ~900 |

### mart_trend_nazionale

```
anno              INTEGER
comuni            BIGINT
avg_stock_pct     DOUBLE
tot_stock_ha      DOUBLE
tot_inc_netto_ha  DOUBLE
tot_inc_lordo_ha  DOUBLE
tot_ripristino_ha DOUBLE
```

### mart_trend_regionale

```
regione           VARCHAR
anno              INTEGER
comuni            BIGINT
avg_stock_pct     DOUBLE
tot_stock_ha      DOUBLE
tot_inc_netto_ha  DOUBLE
tot_inc_lordo_ha  DOUBLE
tot_ripristino_ha DOUBLE
```

### mart_trend_provinciale

```
regione           VARCHAR
provincia         VARCHAR
anno              INTEGER
comuni            BIGINT
avg_stock_pct     DOUBLE
tot_stock_ha      DOUBLE
…
```

## Esempi di analisi possibili

```sql
-- Trend nazionale annuale
SELECT anno, tot_inc_netto_ha
FROM mart_trend_nazionale ORDER BY anno;

-- Regione con più nuovo consumo nel 2024
SELECT regione, tot_inc_netto_ha
FROM mart_trend_regionale
WHERE anno = 2024 ORDER BY tot_inc_netto_ha DESC;

-- Provincia con più alto stock % nel 2024
SELECT provincia, regione, avg_stock_pct
FROM mart_trend_provinciale
WHERE anno = 2024 ORDER BY avg_stock_pct DESC;

-- Confronto consumo/popolazione (con JOIN a popolazione_istat_comunale)
SELECT c.anno, c.pro_com, c.comune, c.incremento_netto_ha, p.popolazione_residente
FROM ispra_consumo_suolo c
JOIN popolazione_istat_comunale_2019_2025 p
  ON c.pro_com = p.codice_istat AND c.anno = p.anno;
```

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run full \
  --config candidates/ispra-consumo-suolo/dataset.yml
```
