# Note — who-is-who-pa

## Stato tecnico

Compose puro con `read_parquet()` diretto da GCS. DuckDB 1.5.4+ legge `https://storage.googleapis.com/` nativamente. Il raw layer è un placeholder (scarica ipa_enti ma non viene usato nel clean).

## Join verificati

- `uo.codice_ipa → enti.codice_ipa`: 23.530 enti su 23.709 hanno UO (99,2% coverage)
- `uo.codice_uni_aoo → aoo.codice_uni_aoo`: join parziale (non tutte le UO hanno AOO associata)
- `uo.codice_uni_uo_padre` → self-join per gerarchia (disponibile ma non espanso nel compose)

## Schema

Tutte le colonne sono VARCHAR (CAST esplicito nei support upstream). Il compose preserva i tipi così come arrivano dai parquet upstream.

## Limiti

- **DAIT non integrato**: il join con `dait_amministratori_locali` (sindaci, assessori) richiede una mappatura tra codice ISTAT (ipa_enti) e codifica DAIT (regione+comune). Il formato dei codici differisce. Soluzione: passare da `comuni_master` come bridge table.
- **MEF partecipazioni non integrato**: join possibile via denominazione ente o codice fiscale, ma non fa parte del perimetro v0.
- **Gerarchia non espansa**: il campo `codice_uni_uo_padre` è preservato ma non è applicata una CTE ricorsiva. L'utente può farlo nella propria query.
- **Uff_eFatturaPA**: ~20k UO sono uffici fittizi per fatturazione elettronica, non corrispondono a uffici reali.

## Policy aggiornamento

Quando i dataset upstream cambiano anno, aggiornare gli URL in `sql/clean.sql`. Il pattern è:
`https://storage.googleapis.com/dataciviclab-clean/{slug}/{anno}/{slug}_{anno}_clean.parquet`
