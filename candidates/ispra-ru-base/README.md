# ispra-ru-base — Rifiuti Urbani ISPRA

**Domanda guida:** Dove si produce più rifiuti e dove si ricicla meglio? Come evolve la raccolta differenziata nel tempo?

**Fonte:** [Catasto Rifiuti ISPRA](https://www.catasto-rifiuti.isprambiente.it/) — Dettaglio comunale
**Formato:** CSV (download diretto HTTP, un file per anno)
**Granularità:** comune
**Copertura:** 2010–2024 (15 anni)

## Schema clean (10 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| anno | INTEGER | Anno di riferimento |
| codice_comune_istat | VARCHAR | Codice ISTAT comune (8 cifre) |
| regione | VARCHAR | Nome regione |
| provincia | VARCHAR | Nome provincia |
| comune | VARCHAR | Nome comune |
| popolazione | BIGINT | Popolazione residente (fonte ISPRA) |
| totale_ru_tonnellate | DOUBLE | Rifiuti urbani totali (t) |
| totale_rd_tonnellate | DOUBLE | Raccolta differenziata (t) |
| percentuale_rd | DOUBLE | % RD (calcolata da ISPRA) |

## Mart disponibili (3)

| Mart | Descrizione | Cardinalità |
|---|---|---|
| `mart_comuni` | Arricchimento kg/abitante + benchmark RD% e kg_ru (media nazionale/regionale, percentile, fascia, distanza %) | ~7.700 righe/anno |
| `mart_sintesi` | Statistiche provinciali (RD% medio pesato, kg procapite, std, min/max) | ~107 righe/anno |
| `mart_trend` | CAGR RD%, delta, pendenza per provincia e regione (multi-anno via glob) | 127 totali |

### mart_comuni — colonne aggiunte (24 totali)

```
kg_ru_per_abitante, kg_rd_per_abitante    — pro-capite
classe_demografica                         — A_MENO_5K … D_OLTRE_50K
media_nazionale_rd, media_regionale_rd     — benchmark territoriale
media_classe_rd                            — benchmark tra simili
percentile_nazionale, fascia_rd            — posizione e giudizio
distanza_media_nazionale_pct               — scostamento %
media_nazionale_kg_ru, media_regionale_kg_ru, percentile_kg_ru
rank_classe_rd                             — ranking nella classe
```

## Esempi

```sql
-- Comuni sopra l'80esimo percentile per RD% in Sicilia (2024)
SELECT comune, percentuale_rd, fascia_rd
FROM mart_comuni
WHERE regione = 'Sicilia' AND anno = 2024 AND percentile_nazionale >= 0.8;

-- Province con RD% in calo (CAGR negativo)
SELECT entita, cagr_rd_pct, segnale_trend_rd
FROM mart_trend
WHERE livello = 'provincia' AND cagr_rd_pct < 0
ORDER BY cagr_rd_pct;
```

## Esecuzione

```bash
cd dataset-incubator
toolkit run full --config candidates/ispra-ru-base/dataset.yml --years 2024
```
