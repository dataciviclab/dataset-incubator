# istat-cittadinanze

**Acquisizioni di cittadinanza italiana per territorio, ex-cittadinanza e processo (2012-2025)** — ISTAT `29_849` via **SDMX**.

## Domanda civica

Chi diventa italiano, **dove**, e attraverso quale percorso? La cittadinanza acquisita è l'esito finale del percorso di integrazione: quante persone la ottengono, da quali paesi di origine, in quali regioni e province, e con quale processo (matrimonio, residenza, altro)?

La tensione: il dibattito misura "gli stranieri" e gli arrivi, ma il dato che racconta l'integrazione **compiuta** è la cittadinanza acquisita — e la sua geografia non è quella degli sbarchi.

## Fonte

- **Ente**: ISTAT — dataflow `29_849` ("Acquisitions of citizenship")
- **Canale**: **SDMX live** (`type: sdmx`, agency `IT1`, flow `29_849` v1.0, endpoint esploradati) — il mirror DBnomics è fermo al 2023, la fonte espone 2024 e 2025. Una sola richiesta (la serie completa, ~2 min)
- **Copertura**: 2012-2025 · **138 territori** (Italia, 5 ripartizioni, 22 regioni, 110 province) · 19 ex-cittadinanze · 4 processi
- **Misura**: acquisizioni di cittadinanza (conteggi)

## Perché vale la pena

- **Territorio**: Eurostat copre la cittadinanza acquisita solo a livello **nazionale** (`MIGR_ACQ`); ISTAT scende a **regione** per l'ex-cittadinanza e a **provincia** per i totali.
- **Processo**: distingue matrimonio / residenza / altro — assente in Eurostat.
- **Cross-check**: IT 2023 = **213.567** acquisizioni, **identico** a Eurostat `MIGR_ACQ` 2023 → le due fonti concordano.

## Output minimo atteso

- Clean parquet + mart analitici: `mart_cittadinanze` (anno × regione × ex-cittadinanza, **quota %**), `mart_cittadinanze_processo` (anno × regione × processo), `mart_cittadinanze_serie` (Italia per anno × processo)
- Numeri chiave: Italia da 65.383 (2012) a 196.955 (2025), con picco 217.448 nel 2024; top ex-cittadinanze 2025: Albania (25.175), Marocco (23.016), Romania (15.564); top province 2025: Milano (20.631), Roma (15.222), Brescia (7.116)

## Perimetro v0

- Tutti i livelli territoriali, marcati in `livello`; la colonna **`aggregato`** marca le righe che NON sono "foglie" (territorio macro o cittadinanza non-paese)
- **Ricetta per numeri corretti**:
  - **Totale nazionale**: `livello='nazionale' AND cittadinanza_codice='WORLD' AND processo_codice='ALL'`
  - **Dettaglio per ex-cittadinanza**: `livello='regione' AND NOT aggregato AND processo_codice='ALL'`
  - ⚠️ **Non sommare senza entrambi i filtri**: `livello='nazionale'` da solo include `WORLD` **e** i paesi (2×)
- **Copertura reale (importante)**: l'ex-cittadinanza è disponibile **solo a nazionale / ripartizione / regione**, e solo per **10 paesi** (più `WORLD`); a **provincia c'è solo il totale** (`WORLD`). La somma dei paesi a regione (2023: 209.877 su 213.567; 2025: 193.380 su 196.955) è quindi **minore** del totale nazionale: è un dettaglio parziale, non un errore.
- `processo` include la riga aggregata `Totale` oltre a Matrimonio/Residenza/Altro
- Solo conteggi (`ACQCITIZ`); esclude `ACQCITIZRATE` (tasso per 1000 abitanti)

## Criterio di promozione

- Mart con dati consistenti su tutti gli anni
- Join validato con un codelist territoriale condiviso (per ora codelist locale)

## Stato

`candidate` — run verificato 2026-11-11 (2012-2025): clean 6.923 righe, mart 3.699 righe, **readiness ready (6/8 ok, 0 fail)**.

## Note tecniche

- I nomi di territori e cittadinanze vengono da codelist locali (`codelists/istat_territori.csv`, `codelists/istat_cittadinanze.csv`), estratte dal metadata della fonte (etichette di fonte).
- `livello` è derivato dalla lunghezza del codice ISTAT (`IT` = nazionale, 3 = ripartizione, 4 = regione, 5 = provincia) — euristica documentata.
- Canale scelto: **plugin nativo `sdmx`** (non `script`). Il plugin fa una sola richiesta e normalizza in CSV lungo (~494 serie/anno × 14 anni = 6.923 righe). Lo `script` resta per dataflow troppo grandi per il fetch seriale (es. `istat-asia-ul`).
