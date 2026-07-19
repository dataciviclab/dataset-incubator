# mef-patrimonio-immobili

Catalogo completo degli immobili pubblici italiani dichiarati dalle PA (censimento MEF).

**Fonte**: MEF Dipartimento Economia — Censimento immobili pubblici PA (art. 2 c. 222 L. 191/2009)
**URL**: 31 ZIP `Imm_*_{year}.zip` da opendata_imm/
**Licenza**: CC-BY 4.0

## Copertura

- 2023: 3.257.044 immobili (100% georeferenziati)
- 2022: ~3M (non processato)

## Granularità

Una riga = unità immobiliare. 51 colonne: anagrafica ente, dati catastali, coordinate, superficie, utilizzo, finalità.

## Schema chiave

- `id_bene` (BIGINT) — PK, usato da detenzioni
- `amministrazione_codice_fiscale` — FK → enti
- `latitudine` / `longitudine` — 100% popolati
- `utilizzo_bene` — stato d'uso (Utilizzato direttamente / Non utilizzato / Inutilizzabile / ...)
- `finalita` — destinazione d'uso (Attività amministrativa/uffici pubblici, Attività didattica, ...)

## Preprocess

`preprocess.py` — legge Dati_Adempimento per l'anno, estrae i nomi dei 31 ZIP, li scarica, unzip e merge in un unico CSV. Gestisce differenze encoding (latin-1/utf-8) e normalizzazione nomi file (spazi→trattini, apostrofi→underscore).

## Join

- `id_bene` → `mef-patrimonio-detenzioni.id_bene`
- `amministrazione_codice_fiscale` → `mef-patrimonio-enti.amministrazione_codice_fiscale`

## Output pipeline

`clean/mef_patrimonio_immobili/{year}/mef_patrimonio_immobili_{year}_clean.parquet`
