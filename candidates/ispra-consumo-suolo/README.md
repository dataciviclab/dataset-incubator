# ispra-consumo-suolo — Consumo di suolo ISPRA

**Domanda guida:** Quali territori continuano a consumare più suolo, e quanto pesa ancora il consumo recente rispetto allo stock già accumulato?

**Fonte:** ISPRA — Consumo di suolo, dinamiche territoriali e servizi ecosistemici — [download](https://www.isprambiente.gov.it/it/attivita/suolo-e-territorio/suolo/il-consumo-di-suolo/consumo_di_suolo_estratto_dati_2025_anni_2006_2024.xlsx)
**Licenza:** CC BY 3.0 IT
**Formato:** XLSX (foglio `Comuni_2006_2024`)
**Granularità:** comune
**Copertura:** 2006–2024, 11 periodi (2 pluriennali + 9 annuali)
**Issue:** [#32](https://github.com/dataciviclab/dataset-incubator/issues/32), [#70](https://github.com/dataciviclab/dataset-incubator/issues/70)

## Formato: long (wide → long)

Una riga per comune × periodo. Stock ricostruito per differenza cumulativa dagli incrementi netti.

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

| Colonna | Descrizione |
|---|---|
| pro_com | Codice ISTAT comune |
| comune, provincia, regione | Riferimenti territoriali |
| periodo | Periodo (es. "2015-2016") |
| anno | Anno finale del periodo |
| incremento_netto_ha, incremento_lordo_ha, ripristino_ha | Flussi nel periodo |
| stock_ha, stock_pct | Stock suolo consumato a fine periodo |

## Mart disponibili (2)

| Mart | Descrizione | Cardinalità |
|---|---|---|
| `mart_comuni` | Benchmark consumo suolo: media nazionale/regionale stock_pct, percentile, fascia, classe consumo, benchmark inc_netto | ~71.000 righe (periodi annuali) |
| `mart_sintesi` | Trend per livello: nazionale/regione/provincia × anno (unifica i vecchi 3 trend separati) | ~1.100 righe |

### mart_comuni — colonne benchmark

```
media_nazionale_stock_pct, media_regionale_stock_pct
std_nazionale_stock_pct, percentile_stock_pct
distanza_media_nazionale_pct
media_nazionale_inc_netto, media_regionale_inc_netto, percentile_inc_netto
fascia_consumo_suolo (ELEVATO/SOPRA_MEDIA/MEDIA/SOTTO_MEDIA/BASSO)
classe_consumo (A_MENO_5 … E_OLTRE_30)
```

## Esempi

```sql
-- Comuni con consumo suolo sotto la media nazionale (2024)
SELECT comune, regione, stock_pct, fascia_consumo_suolo
FROM mart_comuni
WHERE anno = 2024 AND fascia_consumo_suolo IN ('BASSO', 'SOTTO_MEDIA');

-- Regioni con più stock cementificato nel 2024
SELECT entita, avg_stock_pct, tot_stock_ha
FROM mart_sintesi
WHERE livello = 'regione' AND anno = 2024
ORDER BY tot_stock_ha DESC;
```

## Esecuzione

```bash
cd dataset-incubator
toolkit run full --config candidates/ispra-consumo-suolo/dataset.yml --years 2024
```
