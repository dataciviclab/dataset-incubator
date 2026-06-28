# Note tecniche — anac-bandi-gara

## Schema raw

| Anno | Formato | Delim | Encoding | Righe clean | Note |
|---|---|---|---|---|---|---|
| 2016 | CSV in ZIP | `;` | UTF-8 | 332.115 | |
| 2017 | CSV in ZIP | `;` | UTF-8 | 374.234 | |
| 2018 | CSV in ZIP | `;` | UTF-8 | 371.944 | |
| 2019 | CSV in ZIP | `;` | UTF-8 | 369.654 | |
| 2020 | CSV in ZIP | `;` | UTF-8 | 388.451 | |
| 2021 | CSV in ZIP | `;` | UTF-8 | 490.443 | |
| 2022 | CSV in ZIP | `;` | UTF-8 | 490.443 | |
| 2023 | CSV in ZIP | `;` | UTF-8 | 655.125 | |
| 2024 | CSV in ZIP | `;` | UTF-8 | 1.228.909 | |
| 2025 | CSV in ZIP | `;` | UTF-8 | 1.475.581 | |

Espansione 2016-2025 (10 anni), pattern CKAN `cig-{year}` stabile.
Toolkit v1.44.1: raw QA checka null byte solo nei primi 4 KB.
`sample_size: -1` per evitare auto-detection errata di CIG_COLLEGAMENTO (2017).

## Join testati

- `openga_ricorsi_appalto` su `cig` — già integrato dalla fonte OpenGA
- `bdap_anagrafe_enti` su `cf_amministrazione_appaltante` — chiave CF

## Performance

- Raw: 12 file ZIP mensili → 1.23GB (37 risorse CKAN, filtrate a 12 CSV)
- Clean parquet: 330MB (2025), 57 colonne (v2: +cig_collegamento, cui_programma, cod_motivo_cancellazione, tipo_appalto_riservato)
- Mart: ~5.6MB (2025), 611K righe aggregate
- Run time (2025): ~3.5s mart, raw/clean via cache

## Schema coverage

| Layer | Colonne |
|---|---|
| Raw CSV | 61 |
| Clean | **57** (53 v1 + 4 recuperate v2) |
| Non passate | 4 — tutte a bassissima densità (86-99% missing) |

Colonne raw escluse volutamente: `flag_prevalente`, `FLAG_PREV_RIPETIZIONI` (98.7% null), `COD_IPOTESI_COLLEGAMENTO` (86.2% null), `IPOTESI_COLLEGAMENTO` (86.2% null).

## Colonne recuperate (v2, 2026-06-19)

Da issue #514: recuperate 4 colonne raw omesse nello scaffold iniziale.

| Colonna | Missing % | Utilità |
|---|---|---|
| `cig_collegamento` | 99.99% | Tracciare varianti/modifiche tra CIG |
| `cui_programma` | 97.4% | Join con OpenCoesione (CUI) |
| `cod_motivo_cancellazione` | 100% | Codice motivo cancellazione (complementa `motivo_cancellazione` che è sempre NULL) |
| `tipo_appalto_riservato` | 85.3% | Appalti riservati a cooperative sociali, inclusione |

Nota: tutte e 4 hanno alta % null perché sono colonne opzionali del dataset ANAC (varianti, CUI, riserve). I dati presenti sono comunque preziosi per le analisi specifiche.

## Normalizzazioni applicate (v2)

- `motivo_urgenza`: normalizzato con `UPPER()` — eliminati 5 duplicati case-sensitivi
  (es. "non applicabile" / "NON APPLICABILE", "Somma urgenza e protezione civile" / "SOMMA URGENZA E PROTEZIONE CIVILE")
- `funzioni_delegate`: normalizzato con `UPPER()` — eliminati 3 duplicati

## Qualità dati

**`importo_complessivo_gara` è l'importo dell'intera gara, non del lotto**.
Se una gara ha N lotti, l'importo viene ripetuto N volte. Per aggregazioni
usare `importo_lotto`, non `importo_complessivo_gara`.

**Importi elevati — verificare caso per caso**: alcuni importi sopra il
miliardo sono reali (es. `B77825C53E` — €17.37Mld per servizio idrico Puglia
2026-2046, confermato su ANAC), altri sono probabilmente errati
(es. €12.6Mld per formazione Camera Commercio Cagliari). Il mart non filtra:
usa mediana come metrica robusta e `importo_lotto_massimo` per tracciare i
picchi.

CIG da verificare su portale ANAC (`dati.anticorruzione.it`):
- `B737822CB8` — €12.6Mld — Formazione personale Camera Commercio Cagliari
- `B98FB8A800` — €11.1Mld — Buoni pasto Corte dei Conti
- `B683A6EB40` — €9.2Mld — A.O. Rummo Benevento (lotto 13)
- `B7A484F39D` — €7.9Mld — Forniture Liceo Scientifico Silvestri
- `B8B40BE774` — €6.1Mld — ASP Agrigento (emodinamica)
- `B8F7CC264D` — €5.7Mld — Marina Militare (PA 615)
- `B66A1238E3` — €5.4Mld — ASL Salerno (energia elettrica)
- `B641EBD927` — €5.2Mld — Comune Castelguglielmo (pulizie)

## Limiti CI

- `pr-toolkit-check.yml` usa `--sample-bytes 5242880`: le risorse ANAC sono ZIP
  da 66-143MB, lo smoke check scarica solo i primi 5MB → ZIP troncato →
  `BadZipFile`. Lo smoke fallisce ma il full run funziona.
