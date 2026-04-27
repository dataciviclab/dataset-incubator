# Notes

## Tecnico

**Download**: automatizzato via `url_suffix_by_year` in `dataset.yml`. Gli URL AIFA hanno suffisso data per-anno irregolare (`dati{year}_DD.MM.YYYY.csv`).

| Anno | URL suffix | Note |
|------|-----------|------|
| 2018 | `_23.09.2020.csv` | |
| 2019 | `_23.09.2020.csv` | |
| 2020 | `_22.10.2021.csv` | |
| 2021 | `_24.10.2022.csv` | |
| 2022 | `_07.02.2024.csv` | |
| 2023 | `_15.01.2025.csv` | |
| 2024 | `_04.12.2025.csv` | |

**Formato**: CSV pipe-separated (`|`), encoding UTF-8 (2018 ha byte non-UTF-8 → `ignore_errors: true` in clean read).

**Schema** (17 colonne, verificato su 2023 e 2024):
- identificativi: `anno`, `mese`, `codreg`, `regione`
- gerarchia terapeutica: `classe`, `atc1`, `descrizione_atc1`, `atc2`, `descrizione_atc2`, `atc3`, `descrizione_atc3`, `atc4`, `descrizione_atc4`
- flusso tracciabilita: `numero_confezioni_traccia`, `spesa_flusso_tracciabilita`
- flusso convenzionata: `numero_confezioni_convenzionata`, `spesa_convenzionata`

**Clean**: raw-faithful (17 colonne, TRIM su stringhe, nessun filtro). Tutte le righe hanno `spesa_convenzionata` valorizzata — verificato su 2018-2024.

**Mart**: aggregato per `anno x mese x regione x atc4`, include `quota_spesa_regione_pct` (spesa atc4 / totale regionale mensile).

**Granularita**: anno x mese x 21 regioni/PA x classe x ATC4.

## Risultati run (2018-2024)

| Anno | Righe raw | Righe clean | Righe mart |
|------|-----------|-------------|------------|
| 2018 | ~174k | 174.222 | 121.936 |
| 2019 | ~92k | 92.711 | 81.244 |
| 2020 | ~91k | 91.341 | 80.422 |
| 2021 | ~169k | 169.304 | 121.656 |
| 2022 | ~92k | 91.850 | 78.998 |
| 2023 | ~93k | 92.654 | 78.802 |
| 2024 | ~92k | 92.129 | 78.280 |

Nota: 2018 e 2021 hanno ~170k righe clean perche' includono ATC4 aggiuntivi (L4-L5 fluoroanalogici) non presenti negli altri anni.

Totale convenzionata 2023 (nazionale): ~9,87 mld EUR.

## Gate e caveat

- Gate 1 (schema): risolto — 17 colonne verificate direttamente sul file 2023
- `codreg` non allineato a codici ISTAT standard senza lookup
- Convenzionata e tracciabilita sono canali diversi: non sommare in analisi iniziali
- Dati AIFA aggiornati retroattivamente (file hanno timestamp nel nome, non copertura)
- Nessun dettaglio sub-regionale (ASL, distretto, comune)

## Analitico

- Domanda principale: come cambia la spesa convenzionata per ATC4 tra regioni e nel tempo?
- Metriche: `spesa_convenzionata`, `numero_confezioni_convenzionata`, `quota_spesa_regione_pct`
- Comparabilita' tra regioni: richiede normalizzazione per popolazione
- Non sommare convenzionata + tracciabilita: sono flussi diversi
