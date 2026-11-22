# Censimento abitazioni — stock, occupate e non occupate per comune (2019, 2021, 2023)

## Domanda

- Dove sono finite le abitazioni? Lo sfitto italiano e' un fenomeno metropolitano o
  montano/turistico?
- Lo sfitto cresce o e' strutturale? Cambia la geografia tra le edizioni?
- Quanta parte dello stock e' occupata in affitto (solo 2019: unico anno con il dettaglio).

## Dataset

- fonte: ISTAT, Censimento permanente della popolazione e delle abitazioni
- canale: due dataflow SDMX su IstatData, stesso schema CSV
  - `DF_DCSS_ABITAZIONI_TV_1` — stock / occupate / non occupate
  - `DF_DCSS_ABITAZIONI_TV_2` — occupate per titolo di possesso
- chiave raw: `FREQ=A`, tutte le aree, `NUMB_ROOM=TOT`, `USE_FLOOR_SPACEGROUP=ALL`,
  `HEATING_SYSTEM_TYPE=ALL`, `ACCESS_BUILDING=TOTAL`, `TYPE_OF_BUILDING=TOTAL`
- licenza: CC BY 4.0 (ISTAT), nessuna autenticazione
- copertura: **2019, 2021, 2023** — 7.900+ comuni per anno

> [!IMPORTANT]
> Solo il **2021** e' enumerazione completa. **2019 e 2023 sono edizioni campionarie**:
> i valori sono stime, non conteggi. Ogni mart espone la colonna `tipo_rilevazione` per
> non confonderle.

## Perche vale la pena testarlo

- colma il buco sullo **stock abitativo**: prima di questo candidate il Lab non aveva alcun
  dataset sulle abitazioni esistenti
- serie a tre punti per comune (2019/2021/2023): permette di distinguere sfitto strutturale
  e sfitto in movimento
- il dato contraddice l'equazione "casa vuota = casa disponibile": lo sfitto e' concentrato
  in montagna e nelle localita' turistiche, e nello sfitto alto convivono due fenomeni
  opposti (comuni che si svuotano e comuni con seconde case)
- si unisce a `comuni_master` (codici ISTAT, catastale, NUTS) senza crosswalk aggiuntivi

## Output minimo atteso

- `clean`: 96.464 righe, 8 colonne, 2019+2021+2023, gerarchia territoriale esplicita
  (`italia` / `ripartizione` / `regione` / `provincia` / `comune`)
- `mart_comuni_sfitto`: ~7.900 comuni per anno, stock / occupate / non occupate / tasso
- `mart_italia_serie`: 9 righe (3 anni x 3 misure) con `tipo_rilevazione`
- `mart_affitto_2019`: 7.882 comuni, occupate per titolo e quota in affitto

## Verifica (numeri chiave)

| Anno | Abitazioni | Occupate | Non occupate | Sfitto |
|---|---|---|---|---|
| 2019 (campione) | 35.212.922 | 25.346.523 | 9.866.399 | 28,0% |
| 2021 (enumerazione) | 35.271.829 | 25.690.057 | **9.581.772** | **27,2%** |
| 2023 (campione) | 35.610.473 | 26.051.682 | 9.558.791 | 26,8% |

- tasso di sfitto mediano per comune: 35,1% (2019) · 34,6% (2021) · 34,7% (2023)
- la somma dei mart comunali riproduce i totali nazionali in tutti e tre gli anni
- 2.076 comuni restano sopra il 50% di sfitto in tutte e tre le edizioni; solo 198 cambiano
  classe: lo sfitto e' **strutturale**, non un'emergenza in movimento

## Criterio di promozione

- run verde con `toolkit` (3/3 mart, quality score 100 su raw/clean/mart)
- readiness 8/8
- shape dei mart stabile e leggibile da `data-explorer`

## Stato

- candidate implementato e verificato in locale (2026-11-22)
- issue di intake: #946
- serie aggiornata a 2019/2021/2023: il bulk storico (`DCSS_BULK_ABITAZIONI`, fermo
  all'aprile 2023) copriva solo 2019 e 2021 ed e' stato sostituito dai dataflow tabellari

## Prossimo passo

- promozione: join con `comuni_master` per provincia/regione/NUTS nei mart
- valutare `DF_DCSS_HUDW_2_PROV` per epoca di costruzione x stato di occupazione
- analysis pubblica: "Dove sono finite le abitazioni — geografia dello sfitto"
