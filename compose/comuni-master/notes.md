# comuni-master — note tecniche

## Join

- **Chiave per IPA**: codice catastale (Belfiore), via `upper(trim(h.codice_catastale)) = upper(trim(ip.cod_cat))`
- **Chiave per ISTAT CSV**: codice catastale (stessa logica)
- **Perché non codice ISTAT**: i codici ISTAT non coincidono tra SITUAS e IPA per tutte le regioni (es. Cagliari: 118006 in SITUAS vs 092009 in IPA). Il codice catastale è universale.
- **Copertura NUTS**: 7.768/7.894 (98,4%)
- **Copertura IPA**: 7.893/7.894 (99,99%)

## Fonti

| Fonte | Provenienza | Cosa fornisce |
|---|---|---|
| `istat-elenco-comuni` | GCS clean parquet | Anagrafica, superficie, popolazione, altimetria |
| ISTAT CSV | Download via raw HTTP | NUTS 2021/2024, ripartizione, flag capoluogo, codici storici |
| `ipa-enti` | GCS clean parquet | Codici IPA, fiscale, contatti, solo L6 |

## Copertura

| Metrica | Valore |
|---|---|
| Comuni totali | 7.894 |
| Con NUTS3 2021 | 7.768 (98,4%) |
| Con IPA | 7.893 (99,99%) |
| Senza IPA | 1 |
| Capoluoghi | 107 |
| 110pr ≠ 107pr | 112 |
| NUTS 2021 ≠ 2024 | 2 |

## Run

```bash
toolkit run full --config compose/comuni-master/dataset.yml --year 2026
```

## Mantenimento

Quando `istat-elenco-comuni`, `ipa-enti` o l'ISTAT CSV vengono aggiornati, rigenerare.
