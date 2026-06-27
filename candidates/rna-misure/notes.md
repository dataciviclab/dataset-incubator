# Note — RNA Misure

## Note editoriali

- Le Misure definiscono i regimi di aiuto: ogni legge/decreto che autorizza aiuti di Stato
- Collegabili agli Aiuti via `car` (codice misura)
- Dati storici dal 1994 al 2023

## Note tecniche

- **Fonte**: XML del Registro Nazionale Aiuti di Stato (MIMIT)
- **Pipeline**: `rna-aiuti-stato/scripts/full_batch.py --misure`
- **GCS**: `gs://dataciviclab-clean/rna-aiuti-stato/misure/misure.parquet`
- **Deploy**: gestito dal workflow `build-misure` del repo upstream. auto_deploy=false qui.
- **Forma**: unico parquet cumulativo (non partizionato per anno)
