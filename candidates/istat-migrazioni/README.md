# istat-migrazioni

**Immigrazioni per provincia di destinazione (2002-2024)** — ISTAT `28_185_DF_DCIS_MIGRAZIONI_4` via **DBnomics**.

## Domanda civica

Dove si stabiliscono le persone che immigrano in Italia? Le immigrazioni per **provincia di destinazione** dicono dove atterra il flusso, non solo quanto è grande a livello nazionale.

La tensione: il dibattito misura gli **arrivi via mare** (nazionali, concentrati in poche regioni costiere), ma la destinazione effettiva delle iscrizioni anagrafiche è un'altra geografia — Milano, Roma, Torino in testa.

## Fonte

- **Ente**: ISTAT — dataflow `28_185` (sotto-dataset `DF_DCIS_MIGRAZIONI_4`, "Immigrants - province of next residence")
- **Canale**: **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror, nessun rate-limit SDMX
- **Copertura**: **2002-2024** · **142 territori** di destinazione (Italia, ripartizioni, regioni, province)
- **Misura**: immigrazioni = trasferimenti di residenza **dall'estero** (`TREG`, `CHANGE_OF_RESIDENCE=FREIGN`)

## Perché vale la pena

- **Territorio**: Eurostat copre le immigrazioni solo a livello **nazionale** (`MIGR_IMM1CTZ`); ISTAT scende a **provincia di destinazione**.
- **Serie lunga**: 2002-2024 (23 anni).
- **Cross-check con Eurostat** (`MIGR_IMM1CTZ`): IT **identico** per 2019-2023 (2019: 332.778; 2023: 439.658). Nel 2024 ISTAT 434.579 vs Eurostat 451.583 (revisione — da verificare in promozione).

## Output minimo atteso

- Clean parquet + mart `mart_migrazioni` (anno × territorio × livello)
- Numeri chiave 2024: Italia 434.579; top province: Milano (32.814), Roma (25.097), Torino (18.591), Napoli (11.383), Brescia (10.713)

## Perimetro v0

- Tutti i livelli territoriali, marcati in `livello`; la colonna **`aggregato`** marca le righe che NON sono "foglie" (territorio macro o cittadinanza non-paese)
- **Ricetta per numeri corretti**:
  - **Totale nazionale**: `livello='nazionale' AND territorio_codice='IT'`
  - **Dettaglio sommabile**: `livello='provincia' AND NOT aggregato`
  - ⚠️ **Non sommare senza entrambi i filtri**: `WHERE NOT aggregato` da solo somma regione **e** provincia (2×)
- Solo immigrazioni **dall'estero** (`FREIGN`): `CHANGE_OF_RESIDENCE=ALL` includerebbe anche le migrazioni **interne** tra comuni italiani (≈5× più grandi)
- Cittadinanza/età/sesso = totale (dettaglio non disponibile a livello provinciale in questo dataflow)
- **Emigrazioni per provincia di origine** (`DF_DCIS_MIGRAZIONI_7`) → estensione futura

## Criterio di promozione

- Aggiungere le emigrazioni (`_7`) per il saldo migratorio provinciale
- Riconciliazione con Eurostat documentata (2024 da chiarire)

## Stato

`candidate` — run verificato: clean 3.179 righe, mart 3.179, **readiness 8/8**.

## Note tecniche

- `CHANGE_OF_RESIDENCE=FREIGN` è la chiave: senza filtro il flusso include le migrazioni interne e risulta ~5× più grande (IT 2019: 1.818.075 vs 332.778).
- `livello` derivato dalla lunghezza del codice ISTAT (euristica documentata).
