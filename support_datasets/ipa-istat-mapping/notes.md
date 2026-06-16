# IPA↔ISTAT mapping — note tecniche

## Tecnico

- **Fonte IPA**: dump datastore AgID (`https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True`)
  - CSV con delim `,`, encoding UTF-8
  - ~23.700 enti di tutte le categorie (L6=comuni, L33=scuole, L1=ASL, ecc.)
  - Il file richiede `strict_mode=false` + `ignore_errors=true` per via di righe con quoting irregolare
- **Fonte ISTAT**: `https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv`
  - CSV con delim `;`, encoding latin-1, header multi-riga
  - Letto posizionalmente con `header=false`, `skip=1`
  - ~7.900 comuni + righe di riepilogo territoriale

## Join e bug fix

**Bug originale**: il join era su `i.codice_istat = ip.codice_comune_ISTAT`. Tuttavia IPA usa un proprio sistema di codifica per `Codice_comune_ISTAT` che **non coincide con il codice ISTAT standard** per i comuni con codice provincia > 089 (es. Sardegna).

Esempi:
- Cagliari: ISTAT `092006` → IPA `118006`
- Sassari: ISTAT `090045` → IPA `112050`

**Fix (2026-06-16)**: join via **codice catastale (Belfiore)**, universale e presente in entrambe le fonti:
```sql
ON UPPER(trim(i.codice_catastale)) = UPPER(trim(ip.codice_catastale_comune))
```

**Risultato**:
| Metrica | Prima | Dopo |
|---|---|---|
| Comuni con IPA | 7.052 (95,1%) | **7.412 (99,96%)** |
| Sardegna | 0% | **100%** |
| Senza match | 363 | **3** |

I 3 comuni senza match IPA sono verosimilmente cessati o fusi (da verificare).

## Run

```bash
toolkit run raw -c support_datasets/ipa-istat-mapping/dataset.yml -y 2026
toolkit run clean -c support_datasets/ipa-istat-mapping/dataset.yml -y 2026
toolkit run mart -c support_datasets/ipa-istat-mapping/dataset.yml -y 2026
```

- **Run ID**: `20260616T181739Z_f2de0533`
- **Esito**: ✅ SUCCESS (RAW→CLEAN→MART)
- **Righe mart**: 7.415
- **Colonne**: 16
- **Readiness**: ✅

## Limiti noti

- **Soli comuni (L6)**: non copre province, ASL, università, regioni, altri enti PA
- **Fonte IPA via datastore dump**: l'URL contiene un UUID del datastore — potrebbe cambiare
- **ISTAT letto posizionalmente**: se ISTAT modifica la struttura del CSV, lo schema esplode
- **Solo snapshot 2026**: la serie storica richiederebbe download multipli
