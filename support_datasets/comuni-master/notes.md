# comuni-master — note tecniche

## Join

- **Chiave**: codice catastale (Belfiore), via `upper(trim(i.codice_catastale)) = upper(trim(ip.codice_catastale_istat))`
- **Perché non codice ISTAT**: i codici ISTAT non coincidono tra SITUAS e IPA per tutte le regioni (es. Cagliari: 118006 in SITUAS vs 092009 in IPA). Il codice catastale è universale.
- **Copertura**: 7.412/7.894 comuni con IPA (93,9%), Sardegna 360/360 (100%)
- **482 comuni senza IPA**: non presenti in IPA come categoria L6

## Copertura

| Metrica | Valore |
|---|---|
| Comuni totali (ISTAT) | 7.894 |
| Con IPA | 7.412 |
| Senza IPA | 482 |
| Sardegna con IPA | 360/360 |

## Fonti raw

- **ISTAT**: HTTP da GCS (`https://storage.googleapis.com/dataciviclab-clean/istat_elenco_comuni/...`)
- **IPA**: HTTP da GCS (`https://storage.googleapis.com/dataciviclab-clean/ipa_istat_mapping/...`)

## Run

```bash
toolkit run full --config support_datasets/comuni-master/dataset.yml --year 2026
```

## Mantenimento

Quando `istat-elenco-comuni` o `ipa-istat-mapping` vengono aggiornati, rigenerare. Il clean verrà pushato su GCS dal CI.
