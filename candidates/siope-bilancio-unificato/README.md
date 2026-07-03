# siope-bilancio-unificato

Bilancio consolidato entrate/uscite di tutti i comparti SIOPE (PRO, REG, SAN, UNI).
Dato mensile con arricchimento territoriale e classificazione per macro-categoria.

## Fonte

Parquet pubblicato su GCS dal progetto [open-siope](https://github.com/dataciviclab/open-siope),
che scarica i bulk CSV da [SIOPE](https://www.siope.it) e produce il dataset pulito.

## Copertura

- 2021-2026
- 16+ comparti: PRO (comuni/province), REG (regioni), SAN (ASL/AO/IRCCS), UNI (università),
  MON (comunita' montane), CDC (camere di commercio), e altri enti pubblici
- ~18.000 enti
- Granularità: mensile (periodo 01..12)

## Colonne principali

| Colonna | Descrizione |
|---|---|
| `lato` | entrate / uscite |
| `codice_comparto` | PRO, REG, SAN, UNI |
| `anno` | 2021-2026 |
| `periodo` | 01..12 (mese) |
| `codice_ente` | codice SIOPE dell'ente |
| `codice_istat_comune` | codice ISTAT del comune (sede dell'ente) |
| `codice_provincia` / `provincia` / `regione` | territorio |
| `importo` | centesimi di euro |
| `importo_eur` | euro |
| `is_titolo_9` | true = partite di giro (da escludere dai totali) |
| `macro_categoria_v2` | entrate: Imposte proprie, Fondi perequativi, ... |
| `macro_categoria` | uscite: Personale, Acquisto beni, Investimenti, ... |
| `macro_area` | uscite: Spese correnti, Conto capitale, ... |
