# Notes - malasanita-struttura-mortalita

## Stato tecnico

Nel branch `feat/malasanita-mart-hardening` il candidato ha una prima base eseguibile e verificata:

- `A` raw/clean/mart ok
- `C` raw/clean/mart ok
- `D` raw/clean/mart ok
- compose finale `A + C + D` ok

Join finale verificato:
- `join_c_ok = 21/21`
- `join_d_ok = 21/21`

## Architettura adottata

Pattern multi-fonte:

- un source dataset per ogni fonte
- un mart regionale minimo per fonte
- un compose finale che legge solo output gia aggregati

Implementazione attuale (branch `feat/malasanita-v2-euro2013`):

- `sources/a_strutture_asl/sql/mart.sql`
- `sources/c_strutture_ricovero_asl/sql/mart.sql`
- `sources/d_mortalita_istat/sql/mart_regioni_v1.sql` (v1 — baseline `cod_causa=25`)
- `sources/d_mortalita_istat/sql/mart_regioni_v2.sql` (v2 — Euro-2013, 12 cause)
- `sources/d_mortalita_istat/sql/mart_regioni_v3.sql` (v3 — broad age-standardization 30+)
- `sources/a_strutture_asl/sql/mart_compose_regioni_v1.sql`
- `sources/a_strutture_asl/sql/mart_compose_regioni_v2.sql`
- `sources/a_strutture_asl/sql/mart_compose_regioni_v3.sql`

File legacy (non eseguiti dal dataset.yml, mantenuti come riferimento storico):

- `sources/d_mortalita_istat/sql/mart.sql`
- `sources/a_strutture_asl/sql/mart_compose_regioni.sql`

Il compose finale e` agganciato al dataset di `A` per un vincolo del toolkit: il file SQL del mart deve stare sotto la base dir del dataset che lo esegue.

## Fonte D

La fonte `D` e` il punto metodologicamente piu delicato.

Problema verificato:
- sommare tutte le righe del clean sovraconta i decessi

Scelta adottata nella v1 (main):
- `cod_sesso = 3`, `cod_classe_eta = 9`, `cod_titolo_studio = 9`, `cod_causa = 25`
- produce una riga per territorio: mortalita totale 30+

Scelta adottata nella v2 (branch `feat/malasanita-v2-euro2013`):
- stessi filtri su sesso/eta/studio
- `cod_causa IN (2,5,6,7,9,15,16,17,19,20,22,24)` — 12 cause Euro-2013 proxy
- aggregazione: `SUM(decessi)`, `MAX(pop_media)`, tasso grezzo 30+
- `MAX(pop_media)` verificato: e` identico per tutte le cause dello stesso territorio/anno
  (e` la popolazione 30+ di riferimento, non specifica per causa)

Nota denominatore ibrido (documentata in mart.sql e notebook v2):
- il campo `decessi_evitabili_30plus_per_100k_pop_totale` nel compose finale
  usa numeratore 30+ e denominatore pop totale regionale (da fonte A)
- non e` un tasso grezzo canonico, e` un indicatore proxy comparativo inter-regionale

Causa cod_territorio=4 esclusa nel clean:
- cod 4 = Trentino-Alto Adige aggregato
- cod 21 (Bolzano) e 22 (Trento) gia presenti come righe separate
- escludere 4 evita doppio conteggio nel join

## Join regionale

Fonte A e C:
- `codice_regione` a 3 cifre Ministero

Fonte D:
- `cod_territorio` ISTAT a 2 cifre

Mapping usato nel compose:
- `LEFT(codice_regione, 2)` per le regioni ordinarie
- eccezioni:
  - `041 -> 21` Bolzano
  - `042 -> 22` Trento

Nota: nel dataset ISTAT 2022 i codici territoriali sono gia presenti come stringhe a due cifre (`01`-`22`), quindi il join regge senza padding extra. Questa assunzione va comunque ricontrollata se cambia la sorgente.

## Fonte B

Spike chiuso su issue #22. Esito tecnico:

- 6.989 righe, 21 regioni/PA complete, 504 strutture, 65 discipline
- `sources/b_reparti_ricovero/sql/mart.sql` definito; output: `mart_regioni`
- join regionale compatibile: B e C hanno lo stesso formato `codice_regione` a 3 cifre
- a livello regionale B e` tendenzialmente ridondante rispetto a C sui posti letto
  (`posti_letto_utilizzati` B/C differiscono di sole 6 unita sul totale nazionale)
- il valore distintivo di B e` il dettaglio per `codice_disciplina` / `disciplina`, assente in C

**Decisione:** B non entra nel compose regionale principale. Resta fonte separata con `mart_regioni` proprio, utile per analisi su specializzazione/offerta disciplinare in un follow-up dedicato.

## Limiti residui

- `B` ha un mart regionale ma non entra nel compose principale (vedi sezione Fonte B)
- `D` e` ancora un proxy regionale, non la metrica finale desiderata
- i tassi `30+` di `D` non vanno confusi con un denominatore generale di popolazione residente
- il campo `decessi_30plus_per_100k_pop_totale` usa un numeratore `30+` e un denominatore di popolazione totale: e` un indicatore proxy, non un tasso grezzo canonico

## v3 - age-standardizzazione broad 30+

Esito tecnico:

- la fonte `D` espone tre classi età utili per il 30+: `30-69`, `70-84`, `85+`
- questo non consente una standardizzazione piena a bande quinquennali
- consente pero una standardizzazione esplicita broad, aggregando i pesi ESP2013 sulle tre classi disponibili

Pesi usati:

- `30-69` -> `52.500`
- `70-84` -> `11.500`
- `85+` -> `2.500`
- totale `30+` -> `66.500`

Validazione interna:

- applicata al totale cause (`cod_causa=25`), la broad-standardization replica bene il `tasso_std_10000` della fonte su 30+
- correlazione broad vs tasso standardizzato fonte: `~0,99`
- correlazione tasso grezzo vs tasso standardizzato fonte: molto piu bassa (`~0,41`)

Decisione:

- `v2` resta il proxy grezzo 30+ sulle 12 cause Euro-2013
- `v3` aggiunge una metrica piu difendibile per confronto inter-regionale
- `v3` non sostituisce una age-standardization piena a 5 anni, che la fonte non consente
- follow-up aperto su issue `#24`: decidere se `v3` diventa la baseline consigliata

## v2 — stato (branch `feat/malasanita-v2-euro2013`, PR #16)

### Decisione naming (Opzione A — rinomina esplicita)

Adottata Opzione A: nomi espliciti v1/v2 su tutti gli artifact.

| Layer | v1 | v2 | v3 |
|---|---|---|---|
| D mart | `mart_regioni_v1.sql` / `.parquet` | `mart_regioni_v2.sql` / `.parquet` | `mart_regioni_v3.sql` / `.parquet` |
| A compose | `mart_compose_regioni_v1.sql` / `.parquet` | `mart_compose_regioni_v2.sql` / `.parquet` | `mart_compose_regioni_v3.sql` / `.parquet` |
| Notebook | `malasanita_preanalysis_v1.ipynb` | `malasanita_preanalysis_v2.ipynb` | `malasanita_preanalysis_v3.ipynb` |
| Metrica | `decessi_30plus_per_100k_pop_totale` | `decessi_evitabili_30plus_per_100k_pop_totale` | `tasso_std_broad_evitabile_100k_30plus` |

I file `mart.sql` (D) e `mart_compose_regioni.sql` (A) sono marcati LEGACY nel commento di testa.

### Checklist

- [x] definizione esplicita mortalita evitabile da `D` (Euro-2013 proxy, 12 cause)
- [x] artifact v1 e v2 separati — nessuna competizione sullo stesso parquet
- [x] notebook v1 legge `mart_compose_regioni_v1.parquet`
- [x] notebook v2 legge `mart_compose_regioni_v2.parquet`
- [x] placeholder campo mancante chiuso in notebook v2 (cella nota metodologica)
- [x] caveat Molise/Valle d'Aosta su `personale_osp_per_100k` in notebook v2 e README
- [x] smoke test: run mart D (v1+v2) + run mart A (compose v1+v2), verifica parquet e schema
- [x] smoke test colonne: v1 ha `decessi_30plus_per_100k_pop_totale`, v2 ha `decessi_evitabili_30plus_per_100k_pop_totale`, nessuna contaminazione incrociata
- [x] join_c_ok e join_d_ok = 21/21 su entrambi gli artifact
- [x] age-standardizzazione broad 30+ implementata come v3 (`mart_regioni_v3` + `mart_compose_regioni_v3`)
- [x] fonte B: definito `mart_regioni` minimo, join verificato, decisione presa — fuori dal compose principale (vedi sezione Fonte B e issue #22)
