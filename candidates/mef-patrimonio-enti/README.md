# mef-patrimonio-enti

Anagrafe degli enti pubblici con lo stato di adempimento al censimento immobiliare MEF.

**Fonte**: MEF Dipartimento Economia — Censimento immobili pubblici PA (art. 2 c. 222 L. 191/2009)
**URL**: https://www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/immobili_{year}/Dati_Adempimento_Anno_{year}.csv
**Licenza**: CC-BY 4.0

## Copertura

- 2022: 11.196 enti
- 2023: 11.326 enti

## Granularità

Una riga = ente/PA. Colonne: denominazione, CF, localizzazione, n. beni proprietà/detenzione, flag adempimento.

## Preprocess

`preprocess.py` — normalizza encoding (latin-1 vs utf-8 tra anni) e unifica nomi colonna.

## Join

- `amministrazione_codice_fiscale` → `mef-patrimonio-immobili.amministrazione_codice_fiscale`
- `codice_comune` → `mef-patrimonio-immobili.codice_comune_amministrazione`

## Output pipeline

`clean/mef_patrimonio_enti/{year}/mef_patrimonio_enti_{year}_clean.parquet`
