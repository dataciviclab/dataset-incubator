# Scouting Checklist

Questa checklist serve a decidere in fretta se una fonte pubblica merita:

- una Discussion `Datasets`
- un intake diretto
- un ruolo da `support dataset`
- `watchlist`
- scarto

## Procedura minima

1. Parti dalla pagina ufficiale della fonte.
2. Verifica se esiste un file o endpoint realmente accessibile.
3. Controlla formato, granularità e copertura temporale.
4. Chiediti se il dataset regge da solo o solo come supporto a un join.
5. Chiudi con un verdict chiaro.

Se in 10-15 minuti non emergono almeno:

- un file reale o un endpoint credibile
- granularità chiara
- anni disponibili
- una domanda civica plausibile

la fonte non entra subito in intake. Va in `watchlist` o si scarta.

## Controllo rapido dell'accesso

Se vuoi, puoi fare un probe tecnico con:

```bash
toolkit scout-url "<url>"
```

Il comando aiuta a distinguere tra:

- file diretto
- pagina HTML con link candidati
- risposta opaca

Non sostituisce il giudizio umano sul dataset.

## Regole di giudizio

- una fonte che regge da sola vale più di una che richiede subito un join
- se il join è obbligatorio, va scritto tra i rischi
- la domanda civica deve avere tensione reale
- se non riesci a formulare una domanda interessante, il candidate apre male

## Checklist

### 1. Fonte

- ente o fonte ufficiale
- pagina sorgente
- link diretto al file o endpoint
- formato

### 2. Accesso reale

- il file si scarica davvero?
- ci sono redirect?
- serve JavaScript o login?
- il `content-type` è coerente?

### 3. Struttura minima

- granularità: comune / provincia / regione / altro
- anni disponibili
- una riga rappresenta cosa?
- chiave territoriale presente?
- file unico o uno per anno?

### 4. Rischi

- portale opaco
- licenza poco chiara
- formati sporchi
- chiavi territoriali deboli
- output minimo che non regge senza join
- serie storica troppo corta
- metrica difficile da spiegare

### 5. Verdict

- `go Discussion`
- `pronto per intake diretto`
- `support dataset`
- `watchlist`
- `scartare`

## Come classificare una fonte

### `go Discussion`

- file o endpoint trovato
- struttura minima leggibile
- domanda civica plausibile
- costo di accesso ragionevole

### `pronto per intake diretto`

- caso raro
- fonte molto pulita
- perimetro già stretto
- rischio basso

### `support dataset`

- utile per join, contesto o enrich
- non abbastanza forte da reggere un filone da solo

### `watchlist`

- interessante ma troppo opaca o immatura adesso
- aggiungi sempre un trigger di riapertura

### `scartare`

- accesso pessimo
- granularità debole
- metrica troppo confusa
- valore civico limitato rispetto allo sforzo
