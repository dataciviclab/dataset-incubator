# Note tecniche — anac-appalti-master

## Struttura

Preprocess.py con DuckDB:
1. Materializza tutte le tabelle dimensionali aggregate a livello CIG
2. Bandi deduplicati via QUALIFY ROW_NUMBER() (picking max importo_lotto per CIG)
3. Aggiudicazioni, collaudo aggregati via any_value() a 1 riga per CIG
4. Processa ogni anno di bandi con INSERT INTO (evita OOM)

## Join model validato

| Passaggio | Chiave | Tipo |
|---|---|---|
| bandi → aggiudicazioni | `cig` | LEFT JOIN (65% match) |
| aggiudicazioni → aggiudicatari | `id_aggiudicazione` | LEFT JOIN (99.7% match) |
| bandi → partecipanti | `cig` | LEFT JOIN (agg) |
| bandi → subappalti | `cig` | LEFT JOIN (agg) |
| bandi → collaudo | `cig` | LEFT JOIN |
| bandi → SAL | `cig` | LEFT JOIN (agg) |
| bandi → CUP | `cig` | LEFT JOIN |

## Dataset sorgente

| Dataset | Anni | Ruolo |
|---|---|---|
| `anac_bandi_gara` | 2016-2025 | Base: bando |
| `anac_aggiudicazioni` | 2000-2026 | Aggiudicazione |
| `anac_aggiudicatari` | 2000-2026 | Vincitore |
| `anac_partecipanti` | 2023-2026 | Concorrenza (agg) |
| `anac_subappalti` | 2020-2026 | Subappalto (agg) |
| `anac_collaudo` | 2000-2026 | Collaudo |
| `anac_stati_avanzamento` | 2000-2026 | SAL (agg) |
| `anac_cup` | 2000-2026 | Bridge CUP |

## Qualità (run 2026-07-25)

| Metrica | Valore |
|---|---|
| Righe clean | 6.080.637 |
| CIG distinti | 6.080.637 |
| Con vincitore | 3.947.250 (65%) |
| Collaudi | da popolare |

## Performance

| Macchina | RAM | Tempo |
|---|---|---|
| Locale (7.5GB, swap pieno) | 4GB config | ~8 min (raw+clean+mart) |
| CI (GitHub Actions 7GB) | — | ~5 min stimato |
