# Note — RNA Aiuti di Stato

## Note editoriali

- Campione unico in Italia: nessuno ha questi dati in formato queryabile prima d'ora
- Ogni riga = una combinazione Aiuto × Componente × Strumento
- Bootstrap completato: 10 anni, ~17 milioni di righe

## Note tecniche

- **Fonte**: XML del Registro Nazionale Aiuti di Stato (MIMIT), 40 GB di XML trasformati
- **Pipeline**: `rna-aiuti-stato/scripts/full_batch.py` con streaming XML → Parquet
- **Flush periodico**: chunk 50.000 aiuti, RAM picco < 500 MB anche con 4 worker
- **GCS**: `gs://dataciviclab-clean/rna-aiuti-stato/`
- **Deploy**: gestito dal workflow `build` del repo upstream. auto_deploy=false qui.
- **Schedule mensile**: processa solo l'anno corrente (non full)
- **Caveat**: licenza CC BY 4.0 dal MIMIT. Dati sotto-segnalati per agricoltura/pesca (registro separato).
