# farmacie — Anagrafica farmacie italiane (Ministero Salute)

**Dataset**: elenco completo delle farmacie aperte al pubblico in Italia (incluse succursali, dispensari, dispensari stagionali).

**Fonte**: Ministero della Salute — Open Data
https://www.dati.salute.gov.it/it/dataset/farmacie

**Issue**: [#453](https://github.com/dataciviclab/dataset-incubator/issues/453)

## Domanda guida

Distribuzione territoriale delle farmacie in Italia: dove sono i deserti farmaceutici? Densità per comune/ASL/regione, confronto geografico e correlazione con indicatori demografici.

## Dataset

- **Copertura**: snapshot corrente (giugno 2026), aggiornamento **giornaliero**
- **Granularità**: singola farmacia (58.691 records)
- **Join key**: `cod_comune` (codice ISTAT comune)
- **Colonne**: 22 — anagrafica, indirizzo, coordinate, tipologia, date validità
- **Coordinate**: 56.258 (96%) con latitudine/longitudine (OSM)
- **Tipologie**: Ordinaria, Succursale, Dispensario, Stagionale, e altre (9 totali)
- **Copertura**: 7.492 comuni

## Perché vale la pena

- Tema civico forte: i "deserti farmaceutici" sono un indicatore di equità territoriale del SSN
- Include coordinate geografiche per analisi spaziali
- Aggiornamento giornaliero — sempre fresco
- Joinabile con popolazione ISTAT, indicatori sanitari, IRPEF

## Output minimo atteso

- Dataset clean `farmacie_2026_clean.parquet` con anagrafica completa
- Mart aggregato per comune/tipologia (`n_farmacie`)
- Notebook v0: mappa densità farmacie per comune, deserti farmaceutici

## Criterio di promozione

- Run full passato (RAW→CLEAN→MART), readiness 5/5
- Dati coerenti: 58.691 farmacie, 7.492 comuni, 96% coordinate OK
- Mart con conteggio per comune e tipologia

## Limitazioni note

- **URL non stabile**: il filename cambia giornalmente (`FRM_FARMA_5_YYYYMMDD.csv`). Per aggiornamenti futuri serve trovare l'URL corrente dal page-data.json
- **Separatore decimale virgola**: latitudine/longitudine usano la virgola (es. `45,065`). Il clean.sql fa REPLACE(',', '.') per il cast corretto
- **2.433 farmacie senza coordinate**: ~4% del totale non ha geolocalizzazione
- **Include succursali e dispensari**: non solo farmacie ordinarie. Per conteggio "farmacie vere" filtrare per `codice_tipologia = 1`
- **Frequenza giornaliera**: lo snapshot cambia ogni giorno. Bloccare un giorno di riferimento per riproducibilità

## Stato

- ✅ Run full passato (RAW→CLEAN→MART)
- ✅ 58.691 righe, 22 colonne
- ✅ 96% coordinate geografiche
- ✅ Readiness 5/5
- ⏳ Da pubblicare su explorer

## Prossimo passo

- Notebook v0 esplorativo
- Analisi "deserti farmaceutici" in `dataciviclab/analisi/`
