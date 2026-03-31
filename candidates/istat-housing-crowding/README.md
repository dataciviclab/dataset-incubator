# ISTAT densita abitativa per titolo di godimento

## Domanda

- In Italia, quanto e piu alta la densita abitativa media nelle famiglie in affitto rispetto a quelle in proprieta, e come cambia nel tempo?

## Dataset

- fonte: ISTAT SDMX, dataflow `33_179`
- indicatore usato: `ABITAZ_AFFOLL_MED`
- misura: `10` (`per hundred values`)
- provider: `IT1`
- endpoint dati usato nel pilot: `https://esploradati.istat.it/SDMXWS/rest`

## Perche vale la pena testarlo

- e il primo pilot reale del plugin `sdmx` dopo il merge in `toolkit`
- la domanda civica e leggibile anche con un perimetro molto stretto
- il dataset consente un confronto semplice e difendibile tra `rent` e `property`

## Output minimo atteso

- raw: CSV normalizzato dal plugin `sdmx`
- clean: tabella con anno, titolo di godimento e valore numerico
- mart: serie annuale Italia per `rent` vs `property`
- notebook v0: sanity check del mart e primo grafico della serie

## Criterio di promozione

- run reale verde con `toolkit`
- shape del mart stabile e leggibile
- nota metodologica chiara: qui usiamo un indice di densita abitativa, non il tasso binario di sovraffollamento

## Stato

- intake

## Prossimo passo

- verificare se il flow regge un allargamento oltre `IT` senza introdurre latenza o 404 sul fetch
