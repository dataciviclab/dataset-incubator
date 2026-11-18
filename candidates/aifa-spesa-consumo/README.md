# AIFA spesa e consumo farmaceutica

## Domanda

Come cambia tra regioni e nel tempo la spesa farmaceutica per classi terapeutiche,
per il canale della farmaceutica convenzionata (prescrizioni SSN dispensate in farmacia)?

## Dataset

- fonte: AIFA — *Spesa e consumo relativi al flusso della farmaceutica
  convenzionata e degli acquisti diretti*
- copertura: **2016-2025** (10 annualità)
- run verificato: 2016-2025, tutti gli anni `passed`; readiness **7/8** al primo
  run su `out/` vuoto, **8/8** dal secondo run (bug toolkit#550)
- formato sorgente: CSV pipe-separated (`|`), **cp1252**; dal 2025 ZIP con un CSV
- granularità: anno × mese × regione × classe × ATC4
- layout: single-source, una sorgente per anno (AIFA non ha URL template stabile)

## Perché vale la pena

- fonte ufficiale AIFA, base dei rapporti OsMed, aggiornata ogni anno
- serie di 10 anni con schema stabile: si può guardare il trend, non solo lo snapshot
- granularità mensile e regionale completa (21 regioni/PA) e dettaglio ATC4
- incrociabile con la discussione hub #442 (spesa, consumi, differenze regionali)

## Perimetro

**Convenzionata (focus analitico), tracciabilità (presente nel clean per completezza).**
Il clean è raw-faithful e tiene tutte le 17 colonne; i tre mart usano solo la
convenzionata e scartano le righe senza alcuna misura convenzionata. La fonte
segnala l'assenza in due modi diversi — NULL in alcuni anni, `0` in altri
(2018 e 2021) — quindi il filtro guarda i valori, non solo i NULL. Dettaglio
in `notes.md`.

## Output

- `clean` multi-anno raw-faithful (17 colonne, ~165-178k righe all'anno)
- `mart_mensile_regione_atc4` — anno × mese × regione × classe × ATC4, con spesa,
  confezioni e quota % sul totale regionale del mese
- `mart_sintesi_regione_anno` — regione × anno, con costo medio per confezione,
  quota nazionale e rank regionale
- `mart_trend_regione` — una riga per regione sull'intera serie: delta %, CAGR,
  costo medio dell'ultimo anno. È una tabella multi-anno: un solo file a livello
  dataset (`data/mart/aifa_spesa_consumo/mart_trend_regione.parquet`), non una
  copia per anno.

## Criterio di promozione

- il clean è stabile su tutte e 10 le annualità e la chiave del mart è univoca
  (verificato: sì, ogni anno)
- le tre tabelle coprono le domande civiche senza query ad hoc
- la community esprime interesse specifico su una domanda (es. differenze
  regionali di costo per confezione)

## Stato

- **runnable** su tutte le annualità 2016-2025: readiness 7/8 al primo run,
  8/8 dal secondo. Il 7/8 è un falso negativo del toolkit (#550): il mart
  multi-year viene scritto dopo il check per anno
- GATE 1 (schema) e GATE 2 (download) risolti

## Gate aperti

- **[GATE 1 — risolto]** schema ricostruito dai file reali: il "Manuale
  Operativo" linkato da AIFA puntava a un CV Europass.
- **[GATE 2 — risolto]** download per anno, con override `unzip_first_csv`
  solo sul 2025.

## Domande complementari

- quali regioni hanno il costo medio per confezione più alto, e da quando?
- la spesa 2016-2025 cala in valore reale? di quanto, con quale deflatore?
- quali classi terapeutiche crescono di più tra 2016 e 2025?
- il recupero 2023-2025 è volume o prezzo? (confezioni piatte, €/confezione in salita)

## Prossimo passo

- aprire la PR sul candidate (2016-2025, cp1252, 3 mart, notes aggiornate)
- rispondere a hub #442 con i numeri della serie aggiornata
- valutare un deflatore (ISTAT NIC) per la lettura in termini reali
