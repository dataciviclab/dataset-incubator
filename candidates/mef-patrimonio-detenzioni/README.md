# mef-patrimonio-detenzioni

Detenzioni a favore di terzi di immobili pubblici: chi usa beni pubblici e a quali condizioni.

**Fonte**: MEF Dipartimento Economia — Censimento immobili pubblici PA (art. 2 c. 222 L. 191/2009)
**URL**: 31 ZIP `Det_*_{year}.zip` da opendata_det/
**Licenza**: CC-BY 4.0

## Copertura

- 2023: ~630K detenzioni (non processato)
- 2022: ~600K (non processato)

## Granularità

Una riga = detenzione a favore di terzi. 25 colonne.

## Schema chiave

- `id_variazione` (BIGINT) — PK
- `id_bene` (BIGINT) — FK → immobili
- `tipo_detenzione_terzi` — in locazione / in uso gratuito / in concessione / in gestione per conto di
- `canone_annuale` — €/anno
- `data_decorrenza` / `data_scadenza` — periodo
- `soggetto_ricevente_denominazione` — chi beneficia
- `soggetto_ricevente_pa` — True = beneficiario è PA

## Preprocess

`preprocess.py` — stesso pattern di immobili: legge adempimenti, scarica 31 ZIP, unzip, merge.

## Join

- `id_bene` → `mef-patrimonio-immobili.id_bene`
- `amministrazione_codice_fiscale` → `mef-patrimonio-enti.amministrazione_codice_fiscale`

## Output pipeline

`clean/mef_patrimonio_detenzioni/{year}/mef_patrimonio_detenzioni_{year}_clean.parquet`
