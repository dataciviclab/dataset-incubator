# bdap-entrate-stato

Fonte: MEF / Ragioneria Generale dello Stato - OpenBDAP.

Discussion pubblica di riferimento:
- `dataciviclab` Datasets #154

Issue intake:
- `dataset-incubator` #133

## Domanda

- Come cambia la composizione delle entrate dello Stato tra 2008 e 2024, e quanto pesa nelle crisi il ricorso a componenti non tributarie o non ricorrenti?

## Dataset

- fonte: OpenBDAP, export CSV del rendiconto pubblicato delle entrate dello Stato
- copertura sostanziale del file: `2008-2024`
- livello: nazionale
- granularita originaria: `Titolo -> Natura -> Tipologia -> Provento`
- formato: CSV con delimitatore `;`
- encoding da gestire esplicitamente: `cp1252` / `latin-1`
- caveat chiave: il file espone `Previsioni Definitive CP/CS`, non `Accertato` o `Riscosso`

## Perche vale la pena testarlo

- la fonte permette una prima lettura strutturale del bilancio dello Stato su un arco lungo
- il caso ha una domanda civica leggibile e un perimetro stretto per un v0
- il candidate puo stare in DI senza sconfinare subito in analisi completa

## Output minimo atteso

- `clean` con gerarchia contabile e misure CP/CS tipizzate
- `mart` minimo aggregato per `anno x titolo x natura`
- notebook v0 con sanity check sui pesi relativi delle entrate tributarie, extratributarie e da prestiti

## Criterio di promozione

- run reale riuscito sul file ufficiale
- mart leggibile e coerente con il caveat sulle `Previsioni Definitive`
- notebook v0 che mostri almeno una lettura prudente su `2008`, `2020` e `2024`

## Stato

- intake
- runnable

## Prossimo passo

- verificare allineamento della issue intake #133 col perimetro reale del candidate
- rifinire il notebook v0 con una lettura prudente su `Titolo I` e `Titolo IV`
- decidere se il passo successivo resta in `Datasets` oppure apre una `Domande` piu stretta
