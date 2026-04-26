# AIFA spesa e consumo farmaceutica

## Domanda

Come cambia tra regioni e nel tempo la spesa farmaceutica per classi terapeutiche,
per il canale della farmaceutica convenzionata (prescrizioni SSN dispensate in farmacia)?

## Dataset

- fonte principale: AIFA - Spesa e consumo della farmaceutica convenzionata e acquisti diretti
- copertura filone: 2018-2024 (7 file annuali)
- run verificato: 2018-2024 (raw + clean + mart passati, schema stabile)
- formato sorgente: CSV pipe-separated (`|`), UTF-8
- granularita: anno x mese x regione x classe terapeutica x ATC4
- source: singola (single-source, non piu nested in `sources/`)

## Perche vale la pena testarlo

- fonte ufficiale AIFA, replicabile ogni anno
- serie storica lunga (9 anni), schema stabile tra gli anni
- granularita mensile e regionale completa (21 regioni/PA)
- dettaglio ATC4 abbastanza ricco da sostenere analisi civiche serie
- base dati usata nei rapporti OsMed ufficiali

## Perimetro iniziale scelto

**Convenzionata (focus analitico), tracciabilita (presente in clean per completezza).**
Clean raw-faithful: include tutte le 17 colonne. Mart usa solo flusso convenzionata.

## Output minimo atteso

- clean multi-anno (2018-2024) raw-faithful (17 colonne)
- mart mensile per anno x mese x regione x ATC4 con spesa, confezioni e quota %
- notebook v0 con validazione layer e check chiavi GROUP BY

## Criterio di promozione

Promuovere il filone solo se:

- il clean multi-anno e stabile sull'intera serie 2016-2024 (3 anni gia verificati)
- la domanda sulla spesa regionale per classi terapeutiche emerge con chiarezza
- la community esprime interesse specifico

## Stato

- **runnable**: pipeline completa 2018-2024 (raw + clean + mart + notebook v0)
- GATE 1 e GATE 2 risolti

## Gate aperti

- **[GATE 1 - risolto]** nomi colonna verificati sui file reali 2022-2024. Il link "Manuale Operativo"
  sulla pagina AIFA punta a un CV Europass (link rotto), ma il tracciato e leggibile dai nomi colonna.
  Schema stabile tra i 3 anni verificati.
- **[GATE 2 - risolto]** URL di download automatizzati via `url_suffix_by_year` in `dataset.yml`.
  Suffissi per-anno documentati in `notes.md`.

## Domande complementari

- quali regioni spendono di piu pro capite per classe terapeutica?
- dove cresce di piu la spesa per cardiovascolari o diabetici tra 2016 e 2024?
- ci sono classi terapeutiche con consumo in forte calo (possibile effetto biosimilari)?

## Prossimo passo

- pull request: clean raw-faithful (17 colonne), mart, notebook v0, notes aggiornate
- discussione dataciviclab: risultati regionali su spesa convenzionata 2018-2024
- valutare aggiunta 2016-2017 se schema compatibile
