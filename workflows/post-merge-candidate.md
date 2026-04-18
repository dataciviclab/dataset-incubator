---
name: post-merge-candidate
description: Checklist manuale per un maintainer dopo il merge di un candidate in dataset-incubator. Produce clean parquet in GCS.
license: MIT
metadata:
  version: "0.1"
  owner: "DataCivicLab"
  tags: [dataset-incubator, candidate, gcs, push]
---

# Workflow: post-merge-candidate

Workflow manuale da eseguire dopo il merge di una PR candidate in `dataset-incubator`.
Richiede accesso in scrittura a GCS (`dataciviclab-clean`).

## Quando eseguire

Dopo il merge di una PR che aggiunge o aggiorna un candidate in `candidates/{slug}/`.

## Step

1. **Aggiorna il repo locale**
   ```bash
   git pull origin main
   ```

2. **Runnare il candidato con toolkit**
   ```bash
   cd dataset-incubator
   toolkit run all --config candidates/{slug}/dataset.yml
   # oppure per multi-source:
   toolkit run all --config candidates/{slug}/sources/{source}/dataset.yml
   ```
   Verifica che il run completi senza errori e che `out/data/clean/{slug}/` sia popolato.

3. **Push clean su GCS** (dry-run prima)
   ```bash
   # installa dipendenze GCS se non già presenti
   pip install -r requirements-gcs.txt

   python scripts/push_archive.py --layer clean --slug {slug} --dry-run
   python scripts/push_archive.py --layer clean --slug {slug}
   ```

4. **Verifica**
   Il workflow `validate-clean-catalog` parte automaticamente dopo il push. Controlla che passi.

## Note

- Il mart non viene pushato in questo step — va fatto on-demand dopo analisi.
- Se il run fallisce per problemi di fonte (timeout, schema cambiato), apri issue nel repo prima di procedere.
- Il `pipeline_signals.json` si aggiorna automaticamente al merge via CI — non serve aggiornarlo manualmente.
