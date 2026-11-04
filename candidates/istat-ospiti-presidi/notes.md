# Note — istat-ospiti-presidi

## Source-check

- Dataflow `49_62` verificato il 2026-11-04. Nessun `source_check` SO preesistente.
- Discussion "Domanda" non aperta (flusso snello richiesto esplicitamente).

## Canale: DBnomics (non SDMX diretto)

| | |
|---|---|
| Toolkit | `type: dbnomics` — `provider: ISTAT`, `dataset: "49_62"` |
| Perché | il cubo SDMX intero è ~400k righe / 30-40 MB e va in timeout (provato: 180s per 4 MB) |
| Filtro | `DATA_TYPE 80/89/92`, `AGE TOTAL/Y_GE65`, `SEX 9`, `NEED ALL/SELSUFELD/NOSELSUFELD`, `HEALTHCARE_LEVEL ALL/ABS/LOW/MED/HIGH`, `SOCIAL_PROT_FUNCTION 99`, `TYPE_RESID_CARE_CENTRE ALL` |
| Serie risultanti | ~476 (≈7.100 osservazioni) |
| Mirror | verificato identico a ISTAT su 7 serie (totale, 65+, non auto, adulti, minori, stranieri, Lombardia) |
| Anni | 2009–2023 |

## Rischi tecnici

- **Codelist più ampia del dato**: DBnomics espone `REF_AREA` con 12.471 valori
  (tutti i comuni), ma le serie reali sono 28 aree. Non inferire la copertura
  dalla codelist.
- **`NAP` vs `ALL`**: per i dati adulti/anziani le dimensioni "minori" valgono
  `NAP` (non `ALL`); il clean ammette entrambe.
- **Filtro stretto**: allargare `DATA_TYPE`/`AGE` fa crescere rapidamente il
  payload; il perimetro v0 è volutamente minimale.

## Decisioni

- **`is_aggregato` in `mart_anziani_livello`**: true sulla riga di totale
  (`livello_assistenza = ALL`). Evita il doppio conteggio in somma
  (IT 2023: ALL 291.392 = ABS+LOW+MED+HIGH).
- **Esclusi gli aggregati territoriali**: ripartizioni (`ITC`/`ITD`/`ITE`/`ITF`/`ITG`)
  e `ITDA`, per non duplicare le regioni.
- **`ITD1`/`ITD2`** = Bolzano/Bozen e Trento, tenute come "regioni".
- **Occupazione**: non calcolata in v0 (richiede `49_37`); prevista come mart
  successivo dopo il merge di `istat-presidi-residenziali`.

## Verifica (run 2023, serie 2009–2023)

- clean 7.137 righe · mart 330 + 1.649 + 22 righe · readiness **8/8**
- IT 2023: ospiti **385.191**, 65+ **291.392** (75,6%), non autosufficienti
  **238.996** (82,0% dei 65+), stranieri 20.540 (5,3%)
- 65+ per livello: ABS 10.228 · LOW 52.541 · MED 144.947 · HIGH 83.675
- Occupazione potenziale (con `49_37`): 385.191 / 425.780 = **90,5%**
- Trend ospiti totali 2009→2023: Italia −4,7% · Lombardia −19,7% · Campania +14,0%
