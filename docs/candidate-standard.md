# Standard Candidate — dataset-incubator

**Stato**: standard operativo v1 (2026-07-31) — migrazione dei 109 dataset completata
**Contratti di riferimento**: toolkit v1.47 — [`config-schema.md`](https://github.com/dataciviclab/toolkit/blob/main/docs/config-schema.md), [`conventions.md`](https://github.com/dataciviclab/toolkit/blob/main/docs/conventions.md), [`standard-macros.md`](https://github.com/dataciviclab/toolkit/blob/main/docs/standard-macros.md)
**Modello di riferimento**: candidate allineati a v1.47 — `ga-sentenze`, `ga-ordinanze`, `ga-decreti`, `openga-ricorsi-*`, `ispra-ru-base`, `sbarchi-migranti-italia`, `terna-*`

Questo documento definisce il contratto minimo e raccomandato che ogni candidate deve
rispettare. **Non duplica** il contratto toolkit: lo referenzia e aggiunge le convenzioni
specifiche del candidate in `dataset-incubator`.

> **Eseguibile**: `scripts/validate_candidate_structure.py` è il gate unico
> (struttura + config, `strict` — vedi §4). `scripts/batch_by_source.py` orchestra
> preflight/run per fonte. I vincoli qui sotto sono verificati automaticamente.

---

## 1. Layout candidate (obbligatorio — gate CI)

```
candidates/<slug>/                # slug: ^[a-z0-9-]+$   (validator)
├── dataset.yml                   # dataset.name: ^[a-z0-9_]+$   (validator)
├── README.md                     # richiesto dal validator
├── notes.md                      # richiesto dal validator
└── sql/
    ├── clean.sql                 # obbligatorio
    └── mart*.sql                 # almeno 1 in sql/ o sql/mart/   (validator)
```

Verifica automatica: `scripts/validate_candidate_structure.py` (CI, hard failure).
Layout supportati: `single-source`, `multi-source` (sources/), `support-dataset`,
`compose` (mart-only). **Non** è ammesso convivere `dataset.yml` root + `sources/`
(layout `ambiguous` → failure).

---

## 2. Contratto `dataset.yml`

Forma canonica per candidate full pipeline (raw → clean → mart). Composizione completa
dei campi e tipi: `config-schema.md`. Qui: cosa è **obbligatorio** per essere a standard.

### 2.1 Blocco `dataset`

| Campo | Obbligo | Note |
|---|---|---|
| `name` | ✅ | snake_case, uguale allo slug con `-` → `_` |
| `source_id` | ✅ | id della fonte in source-observatory (tracciabilità) |
| `years` | ✅ | lista anni dichiarati |
| `tags` | ✅ | lista kebab-case, descrittiva (es. `[giustizia, contenzioso]`) |
| `category` | ✅ | vocabolario — vedi Appendice A |
| `time_coverage` | ⚠ raccomandato | `{start_year, end_year}` per serie storiche (supportato dal parser) |

### 2.2 `raw`

- almeno una `raw.sources[]`, con `name`, `type` (`http_file`, `ckan`, `sdmx`, `sparql`, `http_post_file`, `local_file`, `script`), `args`, `primary: true` sulla fonte principale.
- `raw.output_policy: overwrite` quando il run deve sovrascrivere (candidate a standard nei batch).

### 2.3 `clean` — forma canonica

```yaml
clean:
  sql: "sql/clean.sql"
  read:
    source: auto          # forma canonica (config-schema.md)
    mode: latest          # latest | all | explicit | largest
    delim: ";"
    encoding: "utf-8"     # PA italiana spesso cp1252
    header: true
    # altri campi SOLO se il parsing reale lo richiede
  required_columns:       # ✅ obbligatorio — nomi colonne OUTPUT del clean.sql
    - anno
    - chiave_principale
  validate:
    min_rows: 100
    not_null:             # ✅ obbligatorio (policy validator)
      - anno
      - chiave_principale
    primary_key:          # ✅ obbligatorio se dichiarabile (deroga: nota in notes.md)
      - anno
      - chiave_principale
```

Note:
- `clean.required_columns` verifica i nomi **dopo** gli alias del `clean.sql`, non i nomi raw.
- `read_mode` top-level (template attuale) è ancora accettato, ma la forma canonica è
  `read.mode` — i candidate allineati usano `read.source` + `read.mode`.
- `read.mode: all` = unisce più file raw in `raw_input` (multi-fonte, es. ga-sentenze).
- `normalize_rows_to_columns` + `columns` per CSV posizionali instabili (vedi conventions.md §4).

### 2.4 `mart`

```yaml
mart:
  tables:
    - name: "mart_esiti_per_sede"
      sql: "sql/mart_esiti_sede.sql"
  required_tables:        # ✅ tabelle essenziali (verifica presenza output)
    - "mart_esiti_per_sede"
  validate:
    table_rules:
      mart_esiti_per_sede:
        required_columns: [anno, codice_sede, totale]
        primary_key: [anno, codice_sede]   # ✅ da GROUP BY del mart.sql
        min_rows: 5
```

- 1 tabella = 1 file SQL (root `sql/` o `sql/mart/`).
- `primary_key` nel `table_rules` deriva dal `GROUP BY` della query.
- Multi-anno: `mart.tables[].years` + `source_layer` (vedi config-schema.md §"output multi-anno").

### Pattern mart raccomandato — `comuni / sintesi / trend` (dai refactor 2026-07)

I refactor di consolidamento (PR #721 #723 #725 #727 #729) hanno standardizzato i mart
per dataset territoriali su 2-4 tabelle organizzate per dimensione analitica:

| Tabella | Grano | Contenuto |
|---|---|---|
| `mart_comuni` | comune × anno | arricchimento + **benchmark territoriale** |
| `mart_sintesi` | regione/provincia × anno | statistiche territoriali aggregate |
| `mart_trend` | regione/provincia × anno | CAGR e delta **multi-anno** (glob su più anni) |
| (extra) `mart_fasce`/`mart_top`/`mart_policy` | per tema | distribuzione fasce, top N, per policy |

**Benchmark territoriale** (fuso in `mart_comuni`, verifica reale su `irpef-comunale`):
`media_nazionale_*`, `media_regionale_*`, `percentile_*`, `rank_regionale_*`, `fascia`.
Serve per contestualizzare ogni comune rispetto al territorio, senza join a runtime.

**Multi-anno**: `mart_trend` aggrega più anni con `mart.tables[].years` (o glob sui clean
parquet). In `table_rules` usa `min_rows: 0` quando 0 righe è un risultato legittimo
(anni senza dati territoriali — caso `openga-ricorsi-appalto`, PR #500).

**`mart.hierarchy`** (feature toolkit #269, NON legacy): genera mart per livelli territoriali
(naz/reg/prv/com) da un solo config. Usata da `mim-alunni-corso-eta`. Va usata quando la
gerarchia territoriale è il prodotto principale; per mart analitici misti restano le tabelle
esplicite.

### 2.5 Esempio minimo completo

```yaml
root: "../../out"
schema_version: 1

dataset:
  name: "ga_sentenze"
  source_id: "openga"
  tags: [giustizia, giustizia-amministrativa, contenzioso]
  category: giustizia
  years: [2023, 2024, 2025, 2026]
  time_coverage: {start_year: 2023, end_year: 2026}

raw:
  output_policy: overwrite
  sources:
    - name: cds
      type: ckan
      args:
        portal_url: "https://openga.giustizia-amministrativa.it"
        dataset_id: "cds-sentenze"
        resource_name: "CDS - Sentenze - {year}"
        filename: "cds-sentenze-{year}.csv"
      primary: true

clean:
  sql: "sql/clean.sql"
  read: {source: auto, mode: all, delim: ",", encoding: "utf-8", header: true}
  required_columns: [anno, codice_sede, numero_ricorso]
  validate:
    min_rows: 100
    not_null: [numero_ricorso, data_pubblicazione]
    primary_key: [codice_sede, numero_provvedimento, numero_ricorso]

mart:
  tables:
    - name: "mart_esiti_per_sede"
      sql: "sql/mart_esiti_sede.sql"
  required_tables: [mart_esiti_per_sede]
  validate:
    table_rules:
      mart_esiti_per_sede:
        required_columns: [anno, codice_sede, esito_provvedimento, totale]
        primary_key: [anno, codice_sede, esito_provvedimento]
        min_rows: 5

validation:
  fail_on_error: true
```

### 2.6 Forme legacy da non usare nei nuovi candidate

| Legacy | Forma canonica |
|---|---|
| `raw.source` | `raw.sources` |
| `raw.sources[].plugin` | `raw.sources[].type` |
| `raw.sources[].id` | `raw.sources[].name` |
| `clean.read: "auto"` | `clean.read.source: auto` |
| `clean.read.csv.*` | `clean.read.*` |
| `clean.sql_path` | `clean.sql` |
| `mart.sql_dir` | `mart.tables[].sql` |
| `bq` | rimuovere |

Queste falliscono subito (non warning). Tabella completa: config-schema.md §"Legacy rimosso".

---

## 3. Contratto SQL

### 3.1 `clean.sql`

- Legge **solo** da `raw_input` (view DuckDB sui file raw).
- Usa le **8 macro standard** (caricate automaticamente): `normalize_string`,
  `cast_int`, `cast_bigint`, `cast_double`, `normalize_italian_number`,
  `normalize_italian_integer`, `decode_flag`, `remove_dot_thousands`.
- `{year}` per l'anno corrente.
- **Mai** referenziare un alias nella stessa SELECT (DuckDB Binder Error —
  caso `elezioni_comunali`); usare subquery/CTE.
- Se `read.decimal: ","`, i numeri sono già parsati: basta `CAST(x AS DOUBLE)`,
  niente `normalize_italian_number`.
- Responsabilità: solo pulizia/typing. Niente aggregazioni (vanno nel mart).

### 3.2 `mart*.sql`

- Legge **solo** da `clean_input` (parquet clean dell'anno corrente, o unione multi-anno).
- 1 file = 1 tabella dichiarata in `mart.tables`.
- Contiene trasformazioni analitiche (GROUP BY, aggregazioni, **benchmark territoriali**), non pulizia raw.
- `primary_key` del `table_rules` = chiavi del `GROUP BY`.

---

## 4. Gate di validazione

| Cosa | Dove | Esito |
|---|---|---|
| Struttura cartella (layout, file obbligatori, slug) | `validate_candidate_structure.py` (CI) | 🔴 hard |
| Contratto `dataset.yml`: parse + campi **+ `source_id`/`tags`/`category` obbligatori** | `validate_candidate_structure.py` → `validate_config` (toolkit), `strict=True` | 🔴 hard (mancanza = failure) |
| Validazione minima clean (`required_columns`, `not_null`) | idem (check strutturale) | 🔴 hard |
| `primary_key` | deroga esplicita — verificare l'unicità sul dato quando il candidate è runnato | 🟡 opzionale |
| Run pipeline (raw → clean → mart) | `toolkit run` | 🔴 hard su fail_on_error |
| Output + regole (min_rows, not_null, primary_key, transition) | run record | 🔴 hard |
| Preflight bulk per fonte | `scripts/batch_by_source.py` (preflight/run) | 🟡 report aggregato |
| Readiness | `toolkit status` | 🟡 informative |

Comandi di verifica locali:

```bash
python scripts/validate_candidate_structure.py    # gate unico struttura+config (strict)
python scripts/batch_by_source.py --fonte <id>    # preflight per fonte
python scripts/batch_by_source.py --all           # preflight su tutti (lento con fonti giù)
```

---

## 5. Docs del candidate

`README.md` (sezioni minime, dal template):

- Domanda civica (con tensione, non descrittiva)
- Dataset / fonte
- Perché vale la pena
- Output minimo atteso
- Criterio di promozione
- Stato / prossimo passo

`notes.md`: quirk della fonte, rischi noti, decisioni metodologiche (es. deroga primary_key).

---

## 6. Checklist PR (candidate)

Derivata da issue #99 (PULL_REQUEST_TEMPLATE) + contratti v1.47:

- [ ] `dataset.yml` con `name`, `years`, `source_id`, `tags`, `category`
- [ ] `validate_candidate_structure.py` senza failure
- [ ] `toolkit run` ok su tutti gli anni dichiarati (dry-run non basta — vedi batch-lessons)
- [ ] `clean.validate` con `required_columns`, `not_null`, `min_rows`, `primary_key` (o deroga)
- [ ] `mart.validate.table_rules` con `primary_key` dai GROUP BY
- [ ] Nessun file dati committato in root candidate (`*.csv`, `*.parquet`, `*.xlsx`)
- [ ] Notebook `{slug}_v0.ipynb`, niente path assoluti, output immagini puliti
- [ ] Issue di intake collegata

---

## 7. Decisioni

| # | Tema | Esito (2026-07-31) |
|---|---|---|
| A | **Grandfathering**: i vincoli valgono per tutti? | **Chiusa** — migrati tutti i 109 dataset (source_id, tags, category, required_columns, not_null) |
| B | **Vocabolario `category`**: chiuso o aperto? | **Chiuso** — 15 valori in Appendice A. Aggiunte solo via standard update |
| C | **Validazione minima**: warning o hard? | **Hard** — `strict=True` nel gate: source_id/tags/category mancanti = failure |
| D | **Notebook v0**: obbligatorio, su richiesta o rimosso? | da decidere (issue #417) |
| E | **`time_coverage`**: documentarlo in `config-schema.md` | da fare nel toolkit |
| F | **Consolidamento mart esistenti**: quali candidate restano da consolidare verso comuni/sintesi/trend? | da pianificare |

---

## Appendice A — Vocabolario `category` (chiuso, 15 valori — 2026-07-31)

| category | Temi coperti | Fonte di riferimento |
|---|---|---|
| `ambiente` | rifiuti, consumo suolo, emissioni, incidentalità, infrastrutture, territorio | ispra, mit, eurostat |
| `energia` | mix elettrico, capacità rinnovabile | terna |
| `giustizia` | giustizia amministrativa, penale, civile | openga, ministero giustizia |
| `immigrazione` | accoglienza, SAI, sbarchi | centri d'italia, ondata |
| `finanza-pubblica` | bilancio stato, IRPEF, IVA, partecipate, fondi UE/PNRR, aiuti di stato, gini | openbdap, mef, opencoesione, fts, italiadomani, rna |
| `sanita` | LEA, spesa farmaceutica, strutture, ricoveri, mortalità | ministero salute, aifa, bdap |
| `welfare-lavoro` | pensioni, occupazione, housing, demografia | inps, istat |
| `appalti` | bandi, aggiudicazioni, subappalti, TED, opere incompiute | anac, ted, mit |
| `istruzione` | alunni, scuole, università | mim, mur |
| `politica` | elezioni, camera, amministratori | eligendo, camera |
| `pa` | anagrafe enti, IPA, conto annuale, comuni-master | agid, openbdap, istat |
| `economia` | imprese (ASIA), PIL, Eurostat economy | istat, eurostat |
| `terzo-settore` | cinque per mille | ade |
| `normativa` | costituzione e corpus legislativo | italia-corpus |
| `trasporti` | immatricolazioni autovetture | aci |

I `tags` sono liberi (kebab-case, descrittivi) e includono la `category` come primo tag.
