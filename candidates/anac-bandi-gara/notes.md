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

## Limiti CI

- `pr-toolkit-check.yml` usa `--sample-bytes 5242880`: le risorse ANAC sono ZIP
  da 66-143MB, lo smoke check scarica solo i primi 5MB → ZIP troncato →
  `BadZipFile`. Lo smoke fallisce ma il full run funziona.
