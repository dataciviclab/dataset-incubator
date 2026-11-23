# Edilizia residenziale pubblica — finanziato, realizzato, assegnato per comune

## Domanda

- Quanti alloggi pubblici sono stati finanziati, quanti realizzati e quanti assegnati?
- In quali territori il percorso finanziamento -> cantiere -> assegnazione si perde?
- Quanto dura un intervento, e quanti non sono piu' realizzabili?

## Dataset

- fonte: Ministero delle Infrastrutture e dei Trasporti, monitoraggio del programma
  art. 4 c. 1 DL 47/2014 (recupero e razionalizzazione degli immobili ERP di Comuni ed ex IACP)
- canale: CSV singolo pubblico, **aggiornato ogni 6 ore** dalla fonte, nessuna autenticazione
- licenza: CC-BY-4.0
- copertura: **5.560 interventi**, 917 comuni, 19 regioni (manca il Trentino-Alto Adige)
- tracciato: importo, alloggi previsti, stato, date lavori, **alloggi assegnati**, sfratti

> [!IMPORTANT]
> La colonna `Descrizione` del CSV contiene il **nome del comune**, non una descrizione
> dell'intervento. Mappata su `comune`.

> [!IMPORTANT]
> `AlloggiAssegnatiNumero = -1` e' un **sentinella amministrativo** per "non dichiarato"
> (48 interventi), non un conteggio. In clean diventa `NULL`: sommarlo come zero o come -1
> falsa il totale.

## Perche vale la pena testarlo

- e' la prima fonte nazionale aperta che chiude la catena **finanziato -> alloggi -> lavori ->
  assegnati** con dettaglio comunale
- rende misurabile una quota di fallimento dichiarata (692 interventi "non piu' realizzabile")
- la forbice territoriale e' ampia e verificabile per regione
- si combina con `opencup_progetti` (7.757 progetti degli enti ACER/ATER/ALER/IACP/ARCA) e con
  ANAC per gare e stati di avanzamento

## Output minimo atteso

- `clean`: 5.560 righe, 20 colonne, date ISO, importi e conteggi numerici, flag
  `date_incoerenti` sui 5 interventi con fine lavori precedente all'inizio
- `mart_comuni_erp`: 917 comuni con interventi, importo, alloggi, assegnati, quota
- `mart_regioni_erp`: regione x stato
- `mart_stati_intervento`: quadro nazionale per stato

## Verifica (numeri chiave)

| Stato | Interventi | Importo | Alloggi previsti | Assegnati | Quota |
|---|---|---|---|---|---|
| Da completare | 2.926 | 341,0 mln | 18.015 | 4.541 | 25,2% |
| Completato | 1.797 | 87,8 mln | 7.120 | 1.962 | 27,6% |
| non più Realizzabile | 692 | 15,4 mln | 922 | 35 | 3,8% |
| Da rivedere | 145 | 7,0 mln | 334 | 31 | 9,3% |
| **Totale** | **5.560** | **451,3 mln** | **26.391** | **6.569** | **24,9%** |

- 6.569 assegnati = somma dei valori dichiarati: i 48 interventi con `-1` sono esclusi, non
  contati come zero
- 451 mln / 26.391 alloggi = **~17.000 € per alloggio**: e' recupero edilizio, non nuova
  costruzione — non usare come costo di costruzione
- durata mediana dichiarata: 43 giorni (Completato), 57 (Da completare), 28 (non realizzabile)

## Criterio di promozione

- run verde con `toolkit` (3/3 mart, quality score 100 su raw/clean/mart)
- readiness 8/8
- shape dei mart stabile e leggibile da `data-explorer`

## Stato

- candidate implementato e verificato in locale (2026-11-23)
- issue di intake: #947

## Prossimo passo

- promozione: join con `comuni_master` per provincia/regione/NUTS e normalizzazione nomi
- analysis: "Edilizia pubblica — dove si perde il percorso"
- il programma copre solo il DL 47/2014 (~451 mln): **PINQuA non e' incluso** e non e'
  isolabile ne' in OpenCUP ne' in OpenCoesione
