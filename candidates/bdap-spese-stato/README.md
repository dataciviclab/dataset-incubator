# bdap-spese-stato

Fonte: MEF / Ragioneria Generale dello Stato - OpenBDAP.

Issue intake:
- `dataset-incubator` #437

## Domanda

- Come cambia la composizione della spesa dello Stato tra il 2008 e il 2024 per missione? Quanto pesano le missioni di protezione sociale, istruzione e sanità sul totale, e come evolve la loro quota nel tempo?

## Dataset

- fonte: OpenBDAP, dump DataStore del Rendiconto Pubblicato — Spese per Amministrazione, Missione, Programma, Macroaggregato
- copertura: `2008–2024` (17 anni, file cumulativo)
- livello: nazionale
- granularità originaria: `Amministrazione → Missione → Programma → Macroaggregato`
- formato: CSV con delimitatore `;`, encoding `cp1252`
- caveat chiave: espone `Previsioni Definitive CP/CS`, non spesa effettiva

## Perché vale la pena testarlo

- gemello funzionale di `bdap_entrate_stato` — stesso periodo, stessa fonte, stesso atto
- permette di confrontare lato entrate e lato spese del bilancio dello Stato
- classificazione per missione consente analisi tematiche (sanità, istruzione, protezione sociale)
- candidate semplice, perimetro stretto, nessuna dipendenza esterna

## Output minimo atteso

- `clean` con gerarchia contabile e misure CP/CS tipizzate
- `mart` aggregato per `anno × missione` con quote percentuali sul totale
- clean raw-faithful, mart analitico

## Criterio di promozione

- run reale riuscito sul file ufficiale
- mart leggibile e coerente con il caveat sulle `Previsioni Definitive`
- almeno una lettura prudente su `Protezione sociale`, `Istruzione` e `Sanità`

## Stato

- intake
- in bootstrap

## Prossimo passo

- completare run di validazione
- verificare coerenza con `bdap_entrate_stato`
