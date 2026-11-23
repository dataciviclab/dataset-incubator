# Edilizia residenziale pubblica — finanziato, realizzato, assegnato per comune

## Domanda

- Quanti alloggi pubblici sono stati finanziati, quanti realizzati e quanti assegnati?
- In quali territori il percorso finanziamento -> cantiere -> assegnazione si perde?
- Quanto dura un intervento, e quanti non sono piu' realizzabili?

## Dataset

- fonte: Ministero delle Infrastrutture e dei Trasporti, monitoraggio del programma
  art. 4 c. 1 DL 47/2014 (recupero e razionalizzazione degli immobili ERP di Comuni ed ex IACP)
- canale: CSV singolo pubblico su `dati.mit.gov.it`, nessuna autenticazione
- **stato della fonte: ferma e parziale.** Il catalogo dichiara "si aggiorna ogni 6 ore", ma
  il file ha `Last-Modified: 2022-03-04` e l'ultimo periodo di monitoraggio e' **2020-04-01**
- **il programma non e' chiuso**: prosegue almeno fino al 2025. La relazione annuale al
  Parlamento (art. 4 c. 9-bis DL 47/2014, Doc. XXVII n. 31, aggiornata al **31/12/2025**)
  riporta **44.825 alloggi ammessi**, **16.464 ultimati**, **6.705 assegnati**, dotazione
  **oltre 814 mln**. Questo candidate copre **26.391 alloggi su 44.825** (59%): e' uno
  snapshot parziale, non lo stato finale del programma
- licenza: CC-BY-4.0
- copertura: **5.560 interventi**, 917 comuni, 19 regioni (manca il Trentino-Alto Adige)
- `Annualita` ("2014-2017", "2014-2024") e' **l'etichetta del programma**, non la copertura
  dei dati: il monitoraggio va dal 2016-10 al 2020-04
- tracciato: importo, alloggi previsti, stato, date lavori, **alloggi assegnati**, sfratti

> [!IMPORTANT]
> La colonna `Descrizione` del CSV contiene il **nome del comune**, non una descrizione
> dell'intervento. Mappata su `comune`.

> [!IMPORTANT]
> Due **sentinelle amministrative** diventano `NULL` in clean, perche' non sono valori:
> `AlloggiAssegnatiNumero = -1` (48 interventi) e le date lavori a `1900-01-01` (1 intervento,
> Rosignano Marittimo). Sommare il `-1` sottrae 48 al totale; trattarlo come zero lascia il
> totale giusto ma trasforma 48 "non dichiarati" in 48 zeri. Nessuno dei due va bene: da qui
> il `NULL`.

## Perche vale la pena testarlo

- e' la prima fonte nazionale aperta che chiude la catena **finanziato -> alloggi -> lavori ->
  assegnati** con dettaglio comunale
- rende misurabile una quota di fallimento dichiarata (692 interventi "non piu' realizzabile")
- la forbice territoriale e' ampia e verificabile per regione
- si combina con `opencup_progetti` (7.757 progetti degli enti ACER/ATER/ALER/IACP/ARCA) e con
  ANAC per gare e stati di avanzamento

## Output minimo atteso

- `clean`: 5.560 righe, 21 colonne, date ISO, importi e conteggi numerici, flag
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
