# Note — istat-presidi-residenziali

## Source-check

- Indagine verificata il 2026-11-04: accesso diretto SDMX confermato (HTTP 200,
  CSV in 2–13s). Nessun `source_check` SO preesistente su RSA/LTC.
- Discussion "Domanda" non aperta su richiesta esplicita (flusso snello).

## Canale

| | |
|---|---|
| Toolkit | `type: sdmx` — agency `IT1`, flow `49_37`, version `1.0` |
| Endpoint | `https://esploradati.istat.it/SDMXWS/rest` |
| Container | `49_37` restituisce tutte le unità di servizio con le 11 dimensioni del DSD `DCIS_PRESIDI1` |
| Grano | IT + 5 ripartizioni + 20 regioni/province autonome (28 codici `REF_AREA`) |
| Anni | 2009–2023 (verificato) |

## Rischi tecnici

- **Il plugin `sdmx` non supporta `startPeriod`/`endPeriod`**: il raw scarica
  l'intera serie a ogni run. Il clean **non** filtra per anno: il parquet del run
  contiene 2009–2023 e i mart producono la serie completa con **un solo fetch**
  (evita il rate-limit ISTAT, ~13s/chiamata).
- **`opensdmx` CLI va in timeout** sul fetch del catalogo ISTAT (non sui dati):
  mappare offline con `vendors/opensdmx/data/constraints/` o usare l'URL data diretto.
- **Risposta regionale disomogenea**: tassi di risposta bassi al Sud (Campania ~48%,
  Sicilia ~41%) → i valori regionali possono sottostimare l'offerta reale.

## Decisioni

- **`TYPE_RESID_CARE_CENTRE` (ASS/COM) non usato nei mart**: la codelist ISTAT
  (`CL_TIPO_STRUTTURASAN1`) etichetta ASS="familiare", COM="comunitario", ma i
  valori (27k vs 398k posti letto) non corrispondono alla ripartizione
  socio-assistenziale/socio-sanitaria del report ISTAT. Ambiguità documentata;
  il perimetro RSA si isola invece con `MAINLY_TARGET_USERS=ELD` × `HEALTHCARE_LEVEL`.
- **Esclusi gli aggregati**: ripartizioni (`ITC`/`ITD`/`ITE`/`ITF`/`ITG`) e `ITDA`
  (Trentino-Alto Adige) per evitare doppi conteggi con le regioni.
- **`ITD1`/`ITD2`** = Bolzano/Bozen e Trento: sono le unità statistiche ISTAT,
  tenute come "regioni".

## Mappature codici (codelist ISTAT)

- `DATA_TYPE` (`CL_TIPO_DATO14`): 70 presidi · 72 presidi/100k · 73 posti letto ·
  75 posti letto/100k · 76 personale retribuito · 78 personale volontario.
- `MAINLY_TARGET_USERS` (`CL_TIPUTENZA1`): `ELD` = anziani 65+.
- `HEALTHCARE_LEVEL` (`CL_COMPARAZ`): `ABS`/`LOW`/`MED`/`HIGH`.
- `LEGAL_STATUS_OF_HOLDER` (`CL_SETTITOLARE`): 1 pubblico · 2 non profit · 3 profit.
- `PROF_STATUS` (`CL_PERSONALE`): professioni del personale.

## Mart

| Mart | Grano | Contenuto |
|---|---|---|
| `mart_sintesi_regione` | area × anno | presidi, posti letto, posti letto/100k, posti letto anziani, quota, personale |
| `mart_posti_letto_regione` | area × utenza × livello assistenza × anno | posti letto |
| `mart_trend` | area | primo/ultimo anno, delta, CAGR, quota anziani |

## Verifica (run 2023, serie 2009–2023)

- clean 29.694 righe · mart 330 + 5.368 + 22 righe · readiness **8/8**
- Italia 2009 → 2023: 711,3 → 722,0 posti letto/100k (+1,5%, CAGR +0,11%)
- Lombardia: 1.075,5 → 864,4 (−19,6%, CAGR −1,55%)
- Campania: 149,5 → 191,4 (+28,0%, CAGR +1,78%) — resta la più bassa
- quota posti letto anziani: 73,2% → 74,2%
