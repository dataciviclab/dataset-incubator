# istat-permessi

**Permessi di soggiorno validi (stock al 1 gennaio) per provincia e cittadinanza (2008-2024)** — ISTAT `29_348_DF_DCIS_PERMSOGG1_5` via **DBnomics**.

## Domanda civica

Quante persone con permesso di soggiorno vivono in Italia, **dove**, e di quale cittadinanza? I permessi validi sono lo **stock** della presenza regolare: non chi arriva, ma chi è già qui con un titolo.

La tensione: gli sbarchi e gli "arrivi" dominano il dibattito, ma la presenza regolare è fatta di milioni di permessi che si rinnovano — e la sua geografia (Milano, Roma in testa) non è quella degli arrivi.

## Fonte

- **Ente**: ISTAT — dataflow `29_348` (sotto-dataset `DF_DCIS_PERMSOGG1_5`, "Province and citizenship")
- **Canale**: **DBnomics** (`type: dbnomics`, provider ISTAT) — mirror, nessun rate-limit SDMX
- **Copertura**: 2008-2024 · **131 territori** (Italia, 5 ripartizioni, 22 regioni, 103 province) · 67 cittadinanze (incluse aree geopolitiche)
- **Misura**: permessi di soggiorno validi (stock, `RESPER` = "residence permits on 1st January")

## Perché vale la pena

- **Territorio**: Eurostat copre i permessi validi solo a livello **nazionale** (`MIGR_RESVALID`); ISTAT scende a **provincia**.
- **Cittadinanza**: 67 voci (paesi + aree geopolitiche).
- **Cross-check con Eurostat** (`MIGR_RESVALID`, 31/12): allineamento quasi esatto per 2020-2021 (ISTAT 1/1/2021 = 3.373.876 ≈ Eurostat 31/12/2020 = 3.373.594; ISTAT 1/1/2022 ≈ Eurostat 31/12/2021), divergenza nei più recenti (revisioni/definizioni — da verificare in fase di promozione).

## Output minimo atteso

- Clean parquet + mart `mart_permessi` (anno × territorio × livello × cittadinanza)
- Numeri chiave 2024: Italia ~3,6M permessi validi; top cittadinanze: Ucraina (385.819), Marocco (371.809), Albania (359.442), Cina (267.090); top province: Milano (467.638), Roma (337.457), Brescia (114.186), Torino (110.575), Napoli (105.871)

## Perimetro v0

- Tutti i livelli territoriali, marcati in `livello` → per sommare senza doppio conteggio filtrare un solo livello
- Solo lo stock totale (`RESPER`): sesso/età/motivo/durata/stato civile = totale
- La dimensione cittadinanza include **aggregati** (aree geopolitiche + totale): per i singoli paesi filtrare i codici ISO-3166 alpha-2 (2 lettere)

## Criterio di promozione

- Mart con dati consistenti su tutti gli anni
- Riconciliazione con Eurostat `MIGR_RESVALID` documentata (allineamento + divergenze recenti)

## Stato

`candidate` — run verificato: clean 145.006 righe, mart 145.006, **readiness 8/8**.

## Note tecniche

- Il sotto-dataset DBnomics `29_348_DF_DCIS_PERMSOGG1_12` (nuovi rilasci per provincia/motivo) **non è pubblicato** su DBnomics (404): il motivo del permesso non è disponibile per provincia in v0.
- `MARITAL_STATUS=99` è l'unico valore presente (= totale), quindi il filtro non perde informazione.
- `livello` derivato dalla lunghezza del codice ISTAT (euristica documentata).
