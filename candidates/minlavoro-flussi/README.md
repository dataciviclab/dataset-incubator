# minlavoro-flussi

## Domanda civica

**Quante persone entrano e escono dal lavoro in Italia, e come cambia la composizione dei contratti?**

Il Ministero del Lavoro riceve le comunicazioni obbligatorie di instaurazione e cessazione inviate da tutte le imprese. Due pubblicazioni separano lo stesso fenomeno: la Nota trimestrale (macro-aree, 2019-2023) e il Rapporto Annuale (regioni, 2021-2023). Nessuna delle due da sola copre l'intero perimetro: la NOTA estende la serie storica, il RA aggiunge geografia regionale e la dimensione trasformazioni.

## Dataset / fonte

- **Fonte**: `lavoro_opendata` — dati.lavoro.gov.it (OData, DataPortal.AI)
- **Gruppi fusi**: Nota trimestrale (21 tabelle) + Rapporto Annuale (56 tabelle)
- **Copertura**: 2019-2023, Italia
- **Unità di analisi**: regione / ripartizione, genere, tipo contratto, settore, età, motivo cessazione

## Perché vale la pena

- **Trasformazioni det→ind**: nessun dataset nel Lab copre quante trasformazioni avvengono per regione/anno (tabelle RA 03.x)
- **Tirocini e somministrazione**: dimensioni assenti da open-inps
- **Serie 2019-2023 fusa**: la NOTA da sola non ha le regioni, il RA da solo inizia nel 2021
- **Join con open-inps**: su (anno, regione, genere) le comunicazioni MinLavoro sono confrontabili con l'Osservatorio INPS

## Output minimo atteso

| Mart | Cosa risponde |
|------|---------------|
| `mart_flussi_anno` | Quante attivazioni/cessazioni per anno × genere × tipo contratto? |
| `mart_flussi_regione` | Come variano i flussi tra regioni? |
| `mart_trasformazioni` | Quanti determinati diventano indeterminati? |
| `mart_gap_genere` | Quanto distano maschi e donne nelle assunzioni? |

## Criterio di promozione

Promuovere a repo dati autonomo quando:
1. La serie viene aggiornata almeno una volta (refresh OData)
2. Il confronto con open-inps produce almeno un finding verificato
3. La dashboard (quando arriva) ha un utente reale

## Stato / prossimo passo

- [x] Config + SQL + extract
- [x] Run locale passato (23.598 righe clean, 4 mart)
- [ ] Aggiornamento serie 2024 (atteso dal RA 2025)
- [ ] Join analitico con open-inps
