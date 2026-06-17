# Note tecniche — anac-bandi-gara

## Schema raw

| Anno | Formato | Delim | Encoding | Righe |
|---|---|---|---|---|
| 2025 | CSV in ZIP | `;` | UTF-8 | ~1.47M |

Altri anni (2007-2024) disponibili in formato misto CSV/JSON/TTL. Da verificare
con `toolkit schema_diff` prima di estendere.

## Join testati

- `openga_ricorsi_appalto` su `cig` — già integrato dalla fonte OpenGA
- `bdap_anagrafe_enti` su `cf_amministrazione_appaltante` — chiave CF

## Performance

- Raw: 12 file ZIP mensili → 1.23GB (37 risorse CKAN, filtrate a 12 CSV)
- Clean parquet: 330MB, 53 colonne
- Mart: ~5.6MB, 611K righe aggregate
- Run time (2025): ~3.5s mart, raw/clean via cache

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
