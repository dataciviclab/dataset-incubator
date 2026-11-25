# ISTAT densita abitativa per titolo di godimento

## Domanda

- In Italia, quanto e piu alta la densita abitativa media nelle famiglie in affitto rispetto a quelle in proprieta, e come cambia nel tempo?
- Come varia la densita per composizione del nucleo (componenti, figli, quintile di reddito)?

## Dataset

- fonte: ISTAT SDMX diretto (`type: sdmx`), dataflow `33_179` v1.0
- indicatore usato: `ABITAZ_AFFOLL_MED`
- misura: `10` (`per hundred values`)
- provider: `IT1`
- endpoint: `https://esploradati.istat.it/SDMXWS/rest` (default ISTAT dal fix toolkit #444)
- definizione usata nel candidate:
  - label SDMX di `DATA_TYPE`: `household crowding index (number of components of household per square meter)`
  - label SDMX di `MEASURE`: `per hundred values`

> [!IMPORTANT]
> Questo candidate usa un indicatore di densita abitativa media.
> Non e il tasso EU-SILC di sovraffollamento binario.

## Canale e recovery (issue #873)

- Il mirror DBnomics esponeva solo i totali (44 righe, sola TENURE_STATUS):
  accettato come limite, non bloccante
- Canale SDMX diretto ripristinato con il fix toolkit #444 (key completa da
  datastructure): raw ~990 righe con breakdown completi
- Nota: ISTAT espone le breakdown SOLO sul totale famiglie (TENURE=99);
  rent/property esistono solo come righe di totale breakdown
- Correzione mapping: secondo le label ISTAT `1=rent (Affitto)`,
  `2=property (Proprietà)` — il mapping precedente (#870) era invertito

## Perche vale la pena testarlo

- la domanda civica e leggibile anche con un perimetro molto stretto
- il dataset consente un confronto semplice e difendibile tra `rent` e `property`
- le breakdown di composizione del nucleo sono di nuovo disponibili nel clean

## Output minimo atteso

- raw: CSV normalizzato dal plugin `sdmx` (con label per dimensione)
- clean: serie complete con breakdown, tenure 1/2 + totale famiglie
- mart: `mart_crowding_tenure_italy` — serie annuale Italia rent vs property
  (righe di totale, 44 righe)

## Criterio di promozione

- run reale verde con `toolkit`
- shape del mart stabile e leggibile
- nota metodologica chiara: qui usiamo un indice di densita abitativa, non il tasso binario di sovraffollamento

## Stato

- candidate — run verde su SDMX diretto (raw 990 · clean 990 · mart 44)
- richiede toolkit con fix key SDMX (dataciviclab/toolkit#501)

## Prossimo passo

- valutare un secondo mart con le breakdown (es. crowding per componenti del nucleo)
- verificare se il flow regge un allargamento oltre `IT` senza introdurre latenza o 404 sul fetch
