# Censimento abitazioni — stock, occupate e non occupate per comune (2021)

## Domanda

- Dove sono finite le abitazioni? Lo sfitto italiano e' un fenomeno metropolitano o
  montano/turistico?
- Quante abitazioni esistono in un comune, quante sono occupate, quante no — e quanto
  lo sfitto e' lontano dall'essere offerta disponibile?
- Quota di abitazioni occupate in affitto per comune (2019): dove si vive in affitto e dove
  in proprieta'?

## Dataset

- fonte: ISTAT, Censimento permanente della popolazione e delle abitazioni
- canale: bulk **`DCSS_BULK_ABITAZIONI`** (`ATTACHED_DATA_FILES`) sul portale IstatData.
  URL pinnato in `dataset.yml`, nessuna autenticazione, licenza CC BY 4.0
- formato: ZIP (736 KB) -> CSV 11,3 MB, pipe-delimited, UTF-8 con BOM, 56.258 righe
- copertura: 8.055 territori, di cui **7.920 comuni**; anni **2019** e **2021**
- misure: `NUM_DW_AV` (abitazioni), `NUM_OCC_DW_AV` (occupate), `NUM_UNOCC_DW_AV`
  (**non occupate**, dato diretto)

> [!IMPORTANT]
> Il dataflow e' annotato `NonProductionDataflow` e **non compare** nel catalogo SDMX
> standard: per questo non era visibile con la discovery normale. L'unica via e' il file
> in `ATTACHED_DATA_FILES`.

## Perche vale la pena testarlo

- colma il buco sullo **stock abitativo**: prima di questo candidate il Lab non aveva alcun
  dataset sulle abitazioni esistenti (solo un indice prezzi e un indice di affollamento)
- il tasso di sfitto e' calcolabile per **7.904 comuni su 7.920**
- il dato contraddice l'equazione "casa vuota = casa disponibile": lo sfitto e' concentrato
  in montagna e nelle localita' turistiche, non nelle citta'
- si unisce a `comuni_master` (codici ISTAT, catastale, NUTS) senza crosswalk aggiuntivi

## Output minimo atteso

- `clean`: 56.258 righe, 15 colonne, 2019 + 2021, gerarchia territoriale esplicita
  (`italia` / `ripartizione` / `regione` / `provincia` / `comune`)
- `mart_comuni_sfitto`: 7.904 comuni, stock / occupate / non occupate / tasso di sfitto
- `mart_italia_serie`: serie nazionale per misura e anno
- `mart_affitto_2019`: 7.879 comuni, occupate per titolo di possesso e quota in affitto

## Verifica (numeri chiave)

| Controllo | Valore |
|---|---|
| Italia 2021 — abitazioni | 35.271.829 |
| Italia 2021 — occupate | 25.690.057 |
| Italia 2021 — non occupate | **9.581.772 (27,2%)** |
| Comuni con tasso di sfitto | 7.904 |
| Mediana tasso di sfitto (tutti i comuni) | 34,6% |
| Mediana tasso di sfitto (comuni >=1.000 abitazioni) | 29,9% |
| Massimi | Foppolo 95,1% · Argentera 95,0% · Valprato Soana 93,5% · Ribordone 93,1% |
| Minimi | Campi Bisenzio 2,7% · Fonte Nuova 2,9% · Lodine 3,3% |
| Quota affitto 2019 (mediana comuni) | 10,8% |

La somma dei mart comunali riproduce esattamente i totali nazionali (35.271.829 /
25.690.057 / 9.581.772): controllo eseguito sul mart, non sul raw.

## Criterio di promozione

- run verde con `toolkit` (3/3 mart, quality score 100 su raw/clean/mart)
- readiness 8/8
- shape dei mart stabile e leggibile da `data-explorer`

## Stato

- candidate implementato e verificato in locale (2026-11-22)
- issue di intake: #946

## Prossimo passo

- promozione: join con `comuni_master` per provincia/regione/NUTS nei mart
- analysis pubblica: "Dove sono finite le abitazioni — geografia dello sfitto"
- valutare l'edizione successiva del censimento permanente quando ISTAT la rilascera'
