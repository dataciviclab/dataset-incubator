# sbarchi-migranti-italia

## Issue
DataCivicLab/dataset-incubator#596

## Fonte dati
Repository GitHub ondata/liberiamoli-tutti → `sbarchi-migranti/dati/`
https://github.com/ondata/liberiamoli-tutti/tree/main/sbarchi-migranti/dati
Dati estratti dal *Cruscotto statistico giornaliero* del Ministero dell'Interno.

## File raw
- `sbarchi-per-giorno.csv`: arrivi giornalieri (settembre 2019–maggio 2026)

## Encoding
UTF-8, delimitatore virgola, header presente. I campi Data hanno formati misti
(`YYYY-MM-DD` e `DD/MM/YYYY`); `TRY_CAST` in DuckDB li gestisce entrambi.

## Semantica del file (importante)

Il file è una **concatenazione di report** (una riga per `(Data, Data_Report)`).
Ogni report riporta i giorni del suo mese fino alla sua data, quindi lo stesso
giorno compare **2–3 volte** (report di metà mese + di fine mese) e il valore può
essere **rivisto** nei consolidamenti (172 date su 2.465 hanno valori diversi tra
i report).

Il `clean.sql` tiene **una riga per giorno** — quella del report più recente
**con valore non nullo** (`WHERE valore IS NOT NULL` *prima* del
`row_number() OVER (PARTITION BY Data ORDER BY Data_Report DESC)`), così un
report futuro con valore vuoto non fa sparire un giorno già consolidato. Il gate
`clean.validate.primary_key: [data_sbarchi]` protegge la dedup.

| | righe | arrivi |
|---|---|---|
| senza dedup (sbagliato) | 3.699 | 752.128 |
| con dedup (corretto) | 2.465 | 502.611 |

## Limiti

- La serie giornaliera si ferma al **report di fine mese**: non recepisce i
  consolidamenti successivi, che onData pubblica nei **totali mensili ufficiali**
  (`sbarchi-mensili.csv`). Es. 2023: 157.651 (mensile) vs 155.515 (giornaliero).
- Dal **giugno 2026** il PDF non ha più la tabella giornaliera: `sbarchi-per-giorno.csv`
  si ferma al **31 maggio 2026** (i mensili proseguono).

## Manutenzione

La fonte viene aggiornata **due volte a settimana** (lun/giovedì) e il file viene
periodicamente **rigenerato** (l'ultima rigenerazione documentata da onData è del
28 ottobre 2026: rimosse 1.095 righe di giorni futuri a 0, aggiunti report, valori
dalle versioni `_v2`). Va aggiornato `time_coverage.end_year` quando onData
pubblica nuovi dati.
