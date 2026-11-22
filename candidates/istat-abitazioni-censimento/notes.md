# Notes

## Tecnico

- Due dataflow SDMX con lo **stesso schema**: il clean li legge insieme con
  `clean.read.mode: all` (con `mode: latest` leggeva solo il primo, e il mart affitto usciva
  vuoto).
- `TV_1` e `TV_2` espongono **entrambi** la riga di totale (`OWNERSHIP_TYPE=ALL`): senza
  `select distinct` nel clean le righe di totale verrebbero duplicate dal merge dei due raw.
  Il 20% di righe "perse" in transizione raw→clean e' esattamente questa deduplica.
- `clean.read.all_varchar: true` obbligatorio: `REF_AREA` contiene codici con zeri iniziali
  (`001001`) che lo sniffing leggerebbe come interi.
- Il bulk storico `DCSS_BULK_ABITAZIONI` (annotato `NonProductionDataflow`, fermo ad aprile
  2023) copriva solo 2019 e 2021. I dataflow tabellari `TV_1`/`TV_2` coprono anche il 2023 ed
  espongono la stessa informazione: il candidate e' stato spostato su quelli.
- `warn_removed_columns: false` in `clean.validate.promotion`: il clean rinomina
  esplicitamente tutte le colonne raw.

## Analitico

- **Solo il 2021 e' enumerazione completa.** 2019 e 2023 sono edizioni campionarie del
  censimento permanente: i valori comunali sono stime. I mart espongono `tipo_rilevazione`
  per rendere esplicito il confronto.
- Il dettaglio per **titolo di possesso esiste solo nel 2019** (in `TV_2`; 2021 e 2023 hanno
  la sola riga `ALL`). Per il 2021 il titolo di godimento esiste come *famiglie* in
  `DF_DCSS_HUDW_1_COM`, non come abitazioni: unita' di analisi diversa, non confrontabile.
- "Non occupata" non significa "disponibile": dentro ci sono seconde case, immobili in
  ristrutturazione, case inagibili, abitazioni in territori senza domanda.
- Lo sfitto e' stabile. Sui comuni presenti in tutte e tre le edizioni (7.892):
  **2.076** restano al **50% o piu'** in tutte, **5.582** sempre sotto, **198** cambiano
  classe (2,5%). La soglia e' `>= 50`: 19 comuni hanno un tasso di esattamente 50,00%
  (arrotondato a 2 decimali) e con `> 50` i valori diventano 2.069 e 196.
  Analisi esterna alla pipeline, riproducibile sui mart:

  ```sql
  with com as (
    select codice_istat_comune, anno, tasso_sfitto_pct
    from read_parquet('out/data/mart/istat_abitazioni_censimento/*/mart_comuni_sfitto.parquet')
  ),
  p as (
    select codice_istat_comune,
           max(case when anno = 2019 then tasso_sfitto_pct end) t19,
           max(case when anno = 2021 then tasso_sfitto_pct end) t21,
           max(case when anno = 2023 then tasso_sfitto_pct end) t23
    from com group by 1 having count(*) = 3
  )
  select count(*) universo,
         count(*) filter (where t19 >= 50 and t21 >= 50 and t23 >= 50) sempre_sopra,
         count(*) filter (where t19 < 50 and t21 < 50 and t23 < 50) sempre_sotto,
         count(*) filter (where (t19 >= 50) <> (t23 >= 50)) cambiano_classe
  from p;  -- 7892 · 2076 · 5582 · 198
  ```

## Cautele

- Il trend nazionale (28,0% -> 27,2% -> 26,8%) e' **fragile**: mescola un'enumerazione e due
  edizioni campionarie con disegni di rilevazione e calibrazioni diverse. Va pubblicato solo
  con questa avvertenza, oppure verificato su una serie omogenea.
- La mediana del tasso di sfitto dipende dalla soglia dimensionale dei comuni: dichiarare
  sempre la popolazione di riferimento.
- 2011 (censimento storico) e' confrontabile con il 2021 come enumerazione, ma le definizioni
  ("occupate da persone residenti" vs "occupate") non sono identiche.
- Nessuna causalita': il tasso di sfitto non spiega i canoni e non e' spiegato dal turismo.
