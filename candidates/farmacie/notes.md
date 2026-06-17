## Tecnico

- Granularità: singola farmacia (58.691 records)
- Fonte: Ministero della Salute, dataset "Farmacie"
- URL: non stabile — filename con data `FRM_FARMA_5_YYYYMMDD.csv`
- Encoding: utf-8, delim: `;`, skip: 0
- Join key: `cod_comune` (codice ISTAT comune a 5 cifre)
- Source ID: `ministero_salute`

## Particolarità del parsing

- **Separatore decimale**: virgola (`,`) per latitudine/longitudine — non il punto standard
  - Fix: `REPLACE("latitudine", ',', '.') AS DOUBLE` nel clean.sql
- **Righe malformate**: alcune righe CSV hanno formato diverso — gestito con `read_mode: robust` (ignore_errors, null_padding)
- **Data fine validità**: in formato `DD/MM/YYYY` o `-` — lasciata come VARCHAR

## Analitico

- 9 tipologie di farmacia: Ordinaria (1), Succursale (2), Dispensario (3), Stagionale (4), e altre
- Roma: 2.209 farmacie (tipologia Ordinaria), Napoli: 1.097, Milano: 1.053
- 7.492 comuni su ~7.900 totali hanno almeno una farmacia

## Anomalie note

1. **2.433 farmacie senza coordinate** (4%) — probabilmente dati storici o inserimenti manuali senza geolocalizzazione
2. **URL non stabile**: cambia giornalmente. Lo snapshot del candidate si riferisce al 2026-06-17
3. **Una stessa farmacia può avere più record** con date diverse (cambio gestione/P.IVA) — la `cod_farmacia` si ripete con `data_inizio_validita` diversa
4. **CAP come BIGINT**: alcuni CAP hanno leading zero (es. 07010) che vengono troncati. Per uso postale serve formattazione

## Cautele

- Snapshot corrente (2026-06-17) — non c'è serie storica. Per trend servono snapshot successivi
- Il dataset cambia giornalmente: replicabilità non garantita su date diverse
- `cap` come BIGINT perde leading zeros — ricostruibile con LPAD se serve
