# comuni-master — note tecniche

## Join

- **Chiave**: `codice_istat` (6 caratteri, zero-padded)
- **Tipo**: LEFT JOIN da ISTAT (7.894 comuni) verso IPA (7.052 con match)
- I comuni senza match IPA sono verosimilmente comuni non censiti in IPA come L6

## Fonti raw

- **ISTAT**: HTTP da GCS (`https://storage.googleapis.com/dataciviclab-clean/istat_elenco_comuni/...`)
- **IPA**: HTTP da GCS (`https://storage.googleapis.com/dataciviclab-clean/ipa_istat_mapping/...`)

## Run

```bash
toolkit run full --config support_datasets/comuni-master/dataset.yml --year 2026
```

## Mantenimento

Quando `istat-elenco-comuni` o `ipa-istat-mapping` vengono aggiornati, rigenerare:
```bash
toolkit run full --config support_datasets/comuni-master/dataset.yml --year 2026
```
Il clean verrà pushato su GCS dal CI.
