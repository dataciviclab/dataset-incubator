# inps-rdc-pdc — Nuclei percettori RDC/PDC per comune (2020)

**Dataset**: nuclei familiari percettori di Reddito di Cittadinanza (RdC) e Pensione di Cittadinanza (PdC) per comune ISTAT, luglio 2020.

**Fonte**: INPS Open Data — CSV diretto
https://servizi2.inps.it/docallegati/Mig/OpenData/CSV/ID-5773.csv

**Issue**: [#435](https://github.com/dataciviclab/dataset-incubator/issues/435)

## Domanda guida

In quali comuni l'incidenza dei nuclei RdC/PdC è più alta rispetto alla popolazione? Come si correla col reddito medio dichiarato (IRPEF) e con altri indicatori socio-economici del Lab?

## Dataset

- **Copertura**: luglio 2020 (singolo snapshot)
- **Granularità**: comune ISTAT (7.976 comuni)
- **Join key**: `codice_catastale` (Belfiore) — arricchito con `codice_istat` (6 cifre), `regione`, `sigla_provincia`, `superficie_km2` dal support `istat_elenco_comuni`
- **Colonne**: 23 (anno, codice_catastale, codice_istat, comune, regione, sigla_provincia, codice_regione, codice_provincia, superficie_km2, nuclei RdC/PdC, importo medio, takeup, popolazione, ecc.)
- **Formato clean**: Parquet, 23 colonne, 7.976 righe

> **Nota importante**: la colonna `codice_istat` del CSV INPS è in realtà il **codice catastale Belfiore** (es. A001 = Abano Terme), non il codice ISTAT numerico. Il join con il catalogo Lab avviene via `codice_catastale`; il `codice_istat` ISTAT (6 cifre) viene dal support `istat_elenco_comuni`.

## Mart

| Mart | Descrizione |
|---|---|
| `mart_incidenza_comune` | Takeup (metrica ufficiale INPS) + incidenza ricalcolata (nuclei/popolazione) per comune. Esclude comuni con popolazione 0 (soppressi/fusi). |
| `mart_sintesi_regione` | Nuclei RdC/PdC, importo medio pesato, incidenza media per regione. |
| `mart_top_comuni` | Benchmark: top comuni per incidenza e per nuclei totali, con rank. |

## Esecuzione

```bash
cd dataset-incubator
toolkit run -c candidates/inps-rdc-pdc/dataset.yml
```

## Perché vale la pena

- Dato unico sulla povertà assoluta a livello comunale
- Si aggancia perfettamente al catalogo esistente (popolazione, IRPEF, rifiuti, consumo suolo, FSC, dipendenti pubblici, AIFA, Consip, Terna)
- RdC/PdC è stato il principale strumento di contrasto alla povertà in Italia (2019-2023)

## Output minimo atteso

- Dataset clean `inps_rdc_pdc_2020_clean.parquet` queryabile via DuckDB
