# Note — RNA Aiuti di Stato

## Note editoriali

- Campione unico in Italia: nessuno ha questi dati in formato queryabile prima d'ora
- Ogni riga = una combinazione Aiuto × Componente × Strumento
- Il dataset è in fase di bootstrap: 8/10 anni completati

## Note tecniche

- **Fonte**: XML del Registro Nazionale Aiuti di Stato (MIMIT)
- **Pipeline**: `rna-aiuti-stato/scripts/full_batch.py` con streaming XML → Parquet
- **GCS**: `gs://dataciviclab-clean/rna-aiuti-stato/`
- **Deploy**: gestito dal workflow `build` del repo upstream. auto_deploy=false qui.
- **Caveat**: i dati sono pubblicati con licenza CC BY 4.0 dal MIMIT
