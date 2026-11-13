# ISTAT — Ospiti dei presidi residenziali socio-assistenziali e socio-sanitari

Chi sono gli ospiti delle strutture residenziali (RSA, case di riposo, comunità):
ospiti totali, anziani 65+ autosufficienti e non autosufficienti, stranieri, per
regione e anno.

Complemento di `istat-presidi-residenziali` (`49_37`): quello misura l'**offerta**
(posti letto), questo misura l'**utenza** (ospiti). Insieme danno l'occupazione.

Il candidate usa `2023` come anno di run: il clean conserva **2009–2023**, così i
mart producono la serie completa con un solo fetch.

## Domanda civica

Quanti anziani non autosufficienti vivono nelle strutture residenziali, e come
cambia il profilo dell'utenza tra le regioni? Il divario Nord-Sud è di offerta,
di bisogno o di entrambi?

## Fonte

- **Ente**: ISTAT — indagine "Le strutture residenziali socio-assistenziali e
  socio-sanitarie"
- **Dataflow**: `49_62` (Ospiti), DSD `DCIS_OSPITIPRESIDI1`
- **Canale**: **DBnomics** (`ISTAT/49_62`) — mirror verificato contro ISTAT
  (ospiti, 65+, non autosufficienti, stranieri, minori, Lombardia: tutti identici)
- **Granularità**: regionale — Italia + 5 ripartizioni + 20 regioni/PA; i mart
  tengono **Italia + 20 regioni**
- **Copertura**: 2009–2023

## Perché vale la pena

- **Colma il buco di `49_37`**: qui `65+ × livello di assistenza` è disponibile
  per **tutte le 28 aree** (in `49_37` solo a livello nazionale). L'intensità
  assistenziale regionale si legge dal lato ospiti.
- Misura gli **anziani non autosufficienti** (238.996 in Italia nel 2023, 82%
  degli ospiti 65+): il vero perimetro RSA dal lato utenti.
- Include **stranieri** e quote, utili per leggere composizione e pressione.

## Output minimo atteso

- `mart_sintesi_regione`: una riga per area e anno — ospiti totali, 65+, non
  autosufficienti, autosufficienti, stranieri, quote.
- `mart_anziani_livello`: ospiti 65+ per area × livello di assistenza
  (`is_aggregato` per non sommare `ALL` con i dettagli).
- `mart_trend`: primo/ultimo anno, delta e CAGR di ospiti totali e non
  autosufficienti per area.

## Criterio di promozione

Serie 2009–2023 completa, mart `sintesi` + `anziani_livello` + `trend`, e join
con `istat-presidi-residenziali` per l'occupazione (ospiti / posti letto).

## Stato / prossimo passo

- Candidate completo: run 2023, readiness **8/8 ready**.
- Serie 2009–2023 nei mart (clean 7.137 righe, mart 2.001 righe).
- Prossimo passo: PR, poi mart occupazione con `49_37`.
