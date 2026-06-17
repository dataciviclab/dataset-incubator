# Note tecniche — anac-bandi-gara

## 🔴 CI blocker: dipendenza toolkit

Questo candidate usa `type: ckan` con `download_all: true` (plugin mergiato in toolkit
PR #382). Richiede **toolkit >= v1.37.0**.

Al momento (`2026-06-17`) dataset-incubator pinna toolkit `v1.35.0` in
`requirements.txt`. Il CI `pr-toolkit-check.yml` installa da `requirements.txt`
quindi **fallirà** finché il pinning non viene aggiornato.

### Fix necessario

```
requirements.txt:
  dataciviclab-toolkit @ git+https://github.com/dataciviclab/toolkit.git@v1.37.0
  lab-connectors[duckdb,gcs] @ git+https://github.com/dataciviclab/lab-connectors.git@v0.15.1
```

### Dipendenze aggiornate in questo commit

- toolkit: `v1.35.0` → **v1.37.0** (bump + PR #382 download_all + PR #385 layer + PR #386 cleanup MCP)
- lab-connectors: `v0.15.0` → **v0.15.1** (allineato a toolkit)

Il tag `v1.37.0` è stato pushato su remote il 2026-06-17. Il CI di DI
dovrebbe ora risolvere la dipendenza correttamente.

## Schema raw

| Anno | Formato | Delim | Encoding | Righe |
|---|---|---|---|---|
| 2025 | CSV | `;` | UTF-8 | ~1.47M |

Altri anni (2007-2024) disponibili in formato misto CSV/JSON/TTL. Da verificare
con `toolkit schema_diff` prima di estendere.

## Join testati

- `openga_ricorsi_appalto` su `cig` — già integrato dalla fonte OpenGA
- `bdap_anagrafe_enti` su `cf_amministrazione_appaltante` — chiave CF

## Performance

- Raw: 1 file ZIP → 12 CSV mensili → 1.23GB
- Clean parquet: 330MB, 53 colonne
- Mart: ~5.6MB, 611K righe
- Run time (2025): ~3.5s mart, raw/clean via cache
