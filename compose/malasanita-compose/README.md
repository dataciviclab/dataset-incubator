# malasanita-compose

Compose puro del filone **malasanita**. Mette insieme 3 candidate flat regionali (A+C+D) e produce 3 mart con diversa metodologia di mortalità.

## Domanda

Le regioni con meno personale sanitario hanno livelli più alti di mortalità evitabile?

## Fonti

| ID | Candidate | Fonte | Output |
|---|---|---|---|
| A | `candidates/strutture-asl` | Ministero della Salute — Strutture e attività ASL | `mart_regioni` (medici, pediatri, residenti per regione) |
| C | `candidates/strutture-ricovero-asl` | Ministero della Salute — Strutture di ricovero per ASL | `mart_regioni` (personale, posti letto, ricoveri per regione) |
| D | `candidates/mortalita-istat-evitabile` | ISTAT — Mortalità per causa | `mart_regioni_v1/v2/v3` (3 metriche di mortalità) |

**B** (reparti-ricovero) è escluso dal compose: ridondante con C sui posti letto aggregati (differenza di 6 unità sul totale nazionale). Il suo valore distintivo è il dettaglio per disciplina, utilizzabile in analisi separate.

## Output

Il compose produce 3 mart regionali (21 righe, una per regione/PA):

| Mart | Mortalità | Metodologia |
|---|---|---|
| `mart_compose_regioni_v1` | `decessi_30plus` — mortalità totale 30+ | Baseline storica (`cod_causa=25`) |
| `mart_compose_regioni_v2` | `decessi_evitabili_30plus` — 12 cause Euro-2013 | Proxy grezzo 30+, tasso non age-standardized |
| `mart_compose_regioni_v3` | `tasso_std_broad_evitabile_100k_30plus` | **Baseline raccomandata** — broad age-standardization 30+ |

Tutti i mart hanno join A+C+D verificato: 21/21 unità territoriali.

## Esecuzione

```bash
# Il toolkit esegue automaticamente i 3 support prima del compose
toolkit run full --config compose/malasanita-compose/dataset.yml
```

## Dipendenze

- Toolkit **>= v1.24.0** (supporto parametro `thousands` per CSV con separatore migliaia)

## Note tecniche

- Il join regionale usa il mapping `codice_regione` (3 cifre, Ministero) → `cod_territorio` (2 cifre, ISTAT): `LEFT(codice_regione, 2)` con eccezioni `041→21` (Bolzano) e `042→22` (Trento)
- Fonte D ha 3 mart separati (v1/v2/v3) con diverse metodologie — il compose li legge tutti con `union_by_name=true` e filtra per versione
- La v3 è la baseline raccomandata per confronti inter-regionali (decisione issue #24)
