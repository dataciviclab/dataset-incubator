# istat-cittadinanze

**Acquisizioni di cittadinanza italiana per territorio, ex-cittadinanza e processo (2012-2023)** — ISTAT `29_849` via **DBnomics**.

## Domanda civica

Chi diventa italiano, **dove**, e attraverso quale percorso? La cittadinanza acquisita è l'esito finale del percorso di integrazione: quante persone la ottengono, da quali paesi di origine, in quali regioni e province, e con quale processo (matrimonio, residenza, altro)?

La tensione: il dibattito misura "gli stranieri" e gli arrivi, ma il dato che racconta l'integrazione **compiuta** è la cittadinanza acquisita — e la sua geografia non è quella degli sbarchi.

## Fonte

- **Ente**: ISTAT — dataflow `29_849` ("Acquisitions of citizenship")
- **Canale**: **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror allineato, **nessun rate-limit SDMX** (la via SDMX live di ISTAT è lenta e fragile: timeout/500 sui flussi grandi)
- **Copertura**: 2012-2023 · **138 territori** (Italia, 5 ripartizioni, 22 regioni, 110 province) · 19 ex-cittadinanze · 4 processi
- **Misura**: acquisizioni di cittadinanza (conteggi)

## Perché vale la pena

- **Territorio**: Eurostat copre la cittadinanza acquisita solo a livello **nazionale** (`MIGR_ACQ`); ISTAT scende a **regione** per l'ex-cittadinanza e a **provincia** per i totali.
- **Processo**: distingue matrimonio / residenza / altro — assente in Eurostat.
- **Cross-check**: IT 2023 = **213.567** acquisizioni, **identico** a Eurostat `MIGR_ACQ` 2023 → le due fonti concordano.

## Output minimo atteso

- Clean parquet + mart `mart_cittadinanze` (anno × territorio × livello × ex-cittadinanza × processo)
- Numeri chiave: Italia da 65.383 (2012) a 213.567 (2023); top ex-cittadinanze 2023: Albania (31.728), Marocco (27.901), Argentina (16.076); top province: Milano (19.788), Roma (10.875), Torino (7.344)

## Perimetro v0

- Tutti i livelli territoriali, marcati in `livello`; la colonna **`aggregato`** marca le righe che NON sono "foglie" (territorio macro o cittadinanza non-paese)
- **Ricetta per numeri corretti**:
  - **Totale nazionale**: `livello='nazionale' AND cittadinanza_codice='WORLD' AND processo_codice='ALL'`
  - **Dettaglio per ex-cittadinanza**: `livello='regione' AND NOT aggregato AND processo_codice='ALL'`
  - ⚠️ **Non sommare senza entrambi i filtri**: `livello='nazionale'` da solo include `WORLD` **e** i paesi (2×)
- **Copertura reale (importante)**: l'ex-cittadinanza è disponibile **solo a nazionale / ripartizione / regione**, e solo per **10 paesi** (più `WORLD`); a **provincia c'è solo il totale** (`WORLD`). La somma dei 10 paesi a regione (2023: 209.877) è quindi **minore** del totale nazionale (213.567): è un dettaglio parziale, non un errore.
- `processo` include la riga aggregata `Totale` oltre a Matrimonio/Residenza/Altro
- Solo conteggi (`ACQCITIZ`); esclude `ACQCITIZRATE` (tasso per 1000 abitanti)

## Criterio di promozione

- Mart con dati consistenti su tutti gli anni
- Join validato con un codelist territoriale condiviso (per ora codelist locale)

## Stato

`candidate` — run verificato: clean 5.927 righe, mart 5.927, **readiness 8/8**.

## Note tecniche

- I nomi di territori e cittadinanze vengono da codelist locali (`codelists/istat_territori.csv`, `codelists/istat_cittadinanze.csv`), estratte dal metadata DBnomics (etichette di fonte).
- `livello` è derivato dalla lunghezza del codice ISTAT (`IT` = nazionale, 3 = ripartizione, 4 = regione, 5 = provincia) — euristica documentata.
- Canale scelto: **plugin nativo `dbnomics`** (non `script`). Lo `script` resta solo per dataflow troppo grandi per il fetch seriale (es. `istat-asia-ul`, ~280k serie); `29_849` ha 678 serie.
