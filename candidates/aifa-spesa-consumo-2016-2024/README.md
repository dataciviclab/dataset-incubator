# AIFA spesa e consumo farmaceutica 2016-2024

## Domanda

Come cambia tra regioni e nel tempo la spesa farmaceutica per classi terapeutiche,
per il canale della farmaceutica convenzionata (prescrizioni SSN dispensate in farmacia)?

## Dataset

- fonte principale: AIFA - Spesa e consumo della farmaceutica convenzionata e acquisti diretti
- copertura filone: 2016-2024 (9 file annuali)
- run verificato: 2022-2024 (clean + mart passati, schema stabile)
- formato sorgente: CSV pipe-separated (`|`), UTF-8-BOM
- granularita: anno x mese x regione x classe terapeutica x ATC4
- source attiva: `sources/a_spesa_consumo/`

## Perche vale la pena testarlo

- fonte ufficiale AIFA, replicabile ogni anno
- serie storica lunga (9 anni), schema stabile tra gli anni
- granularita mensile e regionale completa (21 regioni/PA)
- dettaglio ATC4 abbastanza ricco da sostenere analisi civiche serie
- base dati usata nei rapporti OsMed ufficiali

## Perimetro iniziale scelto

**Solo convenzionata.** Motivazione: il dataset contiene due flussi distinti
(`convenzionata` e `tracciabilita`), con null strutturali nelle colonne dell'altro flusso.
La convenzionata (prescrizioni SSN dispensate in farmacia) e il canale piu leggibile
per una prima analisi civica e non richiede conoscenza del sistema DPC/ospedaliero.
La tracciabilita viene demandata a una eventuale source `b_tracciabilita` solo se
la community ne fa richiesta esplicita.

## Output minimo atteso

- clean multi-anno (2016-2024) su flusso convenzionata
- mart mensile per anno x mese x regione x ATC4 con spesa e confezioni
- notebook v0 con lettura regionale e per classe terapeutica

## Criterio di promozione

Promuovere il filone solo se:

- il clean multi-anno e stabile sull'intera serie 2016-2024 (3 anni gia verificati)
- la domanda sulla spesa regionale per classi terapeutiche emerge con chiarezza
- la community esprime interesse specifico

## Stato

- intake - primo run completato (2022-2024)

## Gate aperti

- **[GATE 1 - risolto]** nomi colonna verificati sui file reali 2022-2024. Il link "Manuale Operativo"
  sulla pagina AIFA punta a un CV Europass (link rotto), ma il tracciato e leggibile dai nomi colonna.
  Schema stabile tra i 3 anni verificati.
- **[GATE 2 - aperto]** URL di download AIFA contengono UUID non parametrici: i file vanno scaricati
  manualmente dalla pagina ufficiale. Gli URL per anno (2016-2024) sono documentati in `notes.md`.
  Anni mancanti da scaricare: 2016-2021.

## Domande complementari

- quali regioni spendono di piu pro capite per classe terapeutica?
- dove cresce di piu la spesa per cardiovascolari o diabetici tra 2016 e 2024?
- ci sono classi terapeutiche con consumo in forte calo (possibile effetto biosimilari)?

## Prossimo passo

- scaricare gli anni mancanti (2016-2021) e verificare stabilita schema su serie lunga
- aprire discussion in `dataciviclab` con i risultati del primo run
- decidere se il filone merita approfondimento intra-regionale o per classe terapeutica
