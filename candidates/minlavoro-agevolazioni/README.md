# minlavoro-agevolazioni

## Domanda civica

**Le agevolazioni fiscali all'assunzione producono più lavoro?**

Il Ministero del Lavoro registra le dichiarazioni di decontribuzione e detassazione che le imprese presentano per assumere a condizioni agevolate. Questo dataset cattura l'offerta di incentivi — il lato domanda dei flussi è in `minlavoro-flussi`.

## Dataset / fonte

- **Fonte**: `lavoro_opendata` — dati.lavoro.gov.it (OData, DataPortal.AI)
- **Gruppo**: Deposito contratti (6 tabelle)
- **Copertura**: 2017-2024, Italia per regione
- **Unità di analisi**: regione × mese/anno × tipo agevolazione

## Perché vale la pena

- **Unica fonte sulle agevolazioni**: nessun dataset nel Lab copre decontribuzione/detassazione
- **Join analitico**: (regione, anno) con `minlavoro-flussi` per misurare se gli incentivi producono attivazioni
- **Serie lunga**: 2017-2024, copre le riforme degli ultimi anni

## Output minimo atteso

| Mart | Cosa risponde |
|------|---------------|
| `mart_agevolazioni_regione` | Quante dichiarazioni per regione × anno × tipo? |
| `mart_agevolazioni_anno` | Come variano nazionalmente decontribuzione e detassazione? |

## Criterio di promozione

Promuovere a repo dati autonomo quando:
1. Il join con flussi produce almeno un finding verificato
2. La serie viene aggiornata con il prossimo deposito contratti

## Stato / prossimo passo

- [x] Config + SQL + extract
- [x] Run locale passato (3.136 righe clean, 2 mart)
- [ ] Join ROI con minlavoro-flussi (agevolazioni → attivazioni per regione)
