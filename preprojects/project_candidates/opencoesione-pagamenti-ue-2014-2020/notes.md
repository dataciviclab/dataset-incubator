# opencoesione-pagamenti-ue-2014-2020 - note

## Fonte

- URL stabile: `https://opencoesione.gov.it/it/opendata/progetti_esteso.zip`
- redirect osservato in intake: `progetti_esteso_20251031.zip`
- formato: CSV dentro ZIP
- separatore: `;`
- colonne: ~201

## Decisione di framing

Non trattare tutto OpenCoesione come mega-progetto.

Primo taglio:

- solo `2014-2020`
- solo progetti con `FINANZ_UE > 0`
- solo output aggregato `regione x tema`

Questo riduce:

- complessita tecnica
- rumore analitico
- rischio di dispersione

## Problemi tecnici gia noti

### FIX NOW

- colonne finanziarie con virgola decimale: usare `REPLACE(..., ',', '.')` + `CAST AS DOUBLE`
- dataset molto grande: evitare carico ingenuo in memoria

### DA VERIFICARE NEL RUN

- encoding in `duckdb` sul file reale
  - il sample letto via Python regge in `utf-8-sig`
  - non forzare `latin1` finche non c'e un errore reale nel run

Esito del run:

- `utf-8` ha retto nel `clean` reale del candidato
- nessun bisogno emerso di forzare `latin1`

### FIX LATER

- valutare se usare `FONDO_COMUNITARIO` come check secondario oltre a `FINANZ_UE > 0`
- chiarire se servono filtri su stati progetto o date
- valutare se limitare ulteriormente il primo output a regioni ordinarie / Mezzogiorno / grandi temi

## Colonne candidate per il clean

- `COD_LOCALE_PROGETTO`
- `CUP`
- `OC_DESCR_CICLO`
- `OC_TEMA_SINTETICO`
- `FONDO_COMUNITARIO`
- `DEN_REGIONE`
- `DEN_PROVINCIA`
- `DEN_COMUNE`
- `OC_STATO_PROGETTO`
- `FINANZ_UE`
- `FINANZ_TOTALE_PUBBLICO`
- `TOT_PAGAMENTI`
- `OC_COSTO_COESIONE`
- `OC_DATA_INIZIO_PROGETTO`
- `OC_DATA_FINE_PROGETTO_PREVISTA`
- `OC_DATA_FINE_PROGETTO_EFFETTIVA`

## Output minimo

Tabella:

- `regione`
- `tema`
- `finanz_ue_tot`
- `tot_pagamenti_tot`
- `ratio_spesa`
- `n_progetti`

## Esito run nel branch

- `raw` OK
- `clean` OK
- `mart` OK
- notebook `v0` aggiunto

Output finale attuale:

- `220` righe `regione x tema`
- escluse:
  - righe multi-regione
  - `AMBITO NAZIONALE`
  - `PAESI EUROPEI`

Primi casi con ratio basso da rivedere:

- `Molise / Trasporti e mobilita`
- `Molise / Ambiente`
- `Emilia-Romagna / Ambiente`
- `Trentino-Alto Adige / Cultura e turismo`

## Prossimo passo minimo

1. fare una query di QA sui casi con `ratio_spesa = 0`
2. costruire una tabella ordinata per regione sul rapporto medio o ponderato
3. notebook `v0` gia presente: usarlo per scegliere il primo taglio pubblico
4. decidere se il filone regge una prima discussion pubblica
