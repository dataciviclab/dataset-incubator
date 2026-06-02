# Note - istat_nonprofit

## Source-check

- Completato il 2026-06-01, esito `go intake`
- Discussion Domanda: https://github.com/orgs/dataciviclab/discussions/316
- Issue intake DI: https://github.com/dataciviclab/dataset-incubator/issues/428
- Issue funnel DCL: https://github.com/dataciviclab/dataciviclab/issues/318

## Tecnico

- **Approccio**: XLSX download diretto (HTTP file). SDMX tentato ma timeout sui dataflow multi-dimensione.
- **Run 2023**: RAW ✅ → CLEAN ✅ → MART ✅
- **Sheet usata**: "22" (Tavola 22 — dati provinciali, skip=1 per rimuovere riga titolo)
- **Output**: `out/data/mart/istat_nonprofit/2023/mart_nonprofit_province.parquet`
- **107 righe**: tutte le province + righe totali/nazionali
- **Dati verificati**: 368.367 istituzioni, 949.200 dipendenti — corrispondono al comunicato ISTAT

## Analitico

- Roma guida per istituzioni (26.253) e dipendenti (113.610)
- Top 5 province per istituzioni: Roma, Milano, Torino, Napoli, Brescia
- La distribuzione territoriale segue il peso demografico ed economico

## Cautele

- **Skip row**: la riga 1 è un titolo, va saltata con `skip: 1` + `header: true`
- **Schema drift**: le XLSX degli anni precedenti potrebbero avere struttura diversa
- **Solo 2023**: per ora. Da aggiungere anni precedenti (2016-2022) quando disponibili
- **XLSX multi-sheet**: ogni tavola è un foglio separato. Per v1 servono altre sheet (1, 2)

## Rischi

- I dati XLSX contengono righe di totale (Italia, ripartizioni) oltre ai dati provinciali
- I nomi colonna contengono spazi e lettere accentate — gestiti in clean.sql
