# mortalita-istat-evitabile

Dataset ISTAT — Disuguaglianze nella mortalità per causa per caratteristiche demografiche, sociali e territoriali.

**Fonte**: https://www.istat.it/tavole-di-dati/disuguaglianze-nella-mortalita-per-causa-in-italia-secondo-caratteristiche-demografiche-sociali-e-territoriali-anno-2022/
**File raw**: `data_base_2022.xlsx` (foglio `d_base_2022`)
**Anno**: 2022
**Licenza**: CC BY 4.0

**Domanda**: Relazione tra dotazione sanitaria regionale e mortalità evitabile.

**Output**: 3 mart con diverse metodologie:

| Mart | Metrica | Metodologia |
|---|---|---|
| `mart_regioni_v1` | `decessi_30plus` | mortalità totale 30+ (baseline storica) |
| `mart_regioni_v2` | `decessi_evitabili_30plus` | Euro-2013 proxy, 12 cause, tasso grezzo 30+ |
| `mart_regioni_v3` | `tasso_std_broad_evitabile_10000_30plus` | broad age-standardization 30+ ⭐ |

**Note tecniche**: 
- Escluso cod_territorio=4 (Trentino-Alto Adige aggregato, doppio conteggio).
- Filtro: solo righe con cod_sesso=3 (totale), cod_classe_eta=9 (30+), cod_titolo_studio=9 (totale).
- v3 è la baseline raccomandata per confronti inter-regionali (issue #24).
