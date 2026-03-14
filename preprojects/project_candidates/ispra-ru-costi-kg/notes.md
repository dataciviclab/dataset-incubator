# Notes - ispra-ru-costi-kg

## Stato tecnico

Branch di lavoro iniziale:

- `feat/ispra-ru-cross-intake`

Stato attuale:

- intake aperto su issue `#30`
- struttura candidate avviata
- nessun `dataset.yml` ancora definito
- `dataset.yml` iniziali definiti per `A/B/C`
- `clean` e `mart` minimi definiti per `A/B/C`

## Architettura adottata

Pattern multi-fonte:

- `sources/a_ru_base`
- `sources/b_kg_per_abitante`
- `sources/c_costo_per_abitante`
- `compose/` finale per il cross

Scelta adottata:

- i tre `source dataset` sono stati formalizzati con anni `2020-2024`
- `A` RU base eseguito con successo su `2020-2024`
- `B` kg per abitante eseguito con successo su `2020-2024`
- `C` costo per abitante eseguito con successo su `2020-2024`
- per `B/C` il parser robusto e` stato reso esplicito nel `dataset.yml` per gestire le note testuali in coda ai CSV
- primo `compose` minimo definito in `sources/a_ru_base/sql/mart_cross_comuni.sql`
- il `compose/` finale resta ancora da chiudere
- il gate vero resta la verifica di:
  - chiavi di join
  - overlap temporale
  - qualita comparativa delle metriche

## Provenienza

Contesto legacy utile:

- `dataciviclab/projects/progetto-pilota.md`

Asset da recuperare o ricontrollare:

- parsing del dataset RU base gia emerso nel pilota
- anni effettivamente disponibili per `kg per abitante`
- anni effettivamente disponibili per `costo per abitante`
- livello territoriale reale e stabilita delle chiavi

## Rischi noti

- mismatch di granularita o nomenclatura territoriale
- overlap temporale troppo corto tra le tabelle
- `costo per abitante` non direttamente confrontabile senza caveat ulteriori
- possibile valore diverso dei due dataset aggiuntivi:
  - vero asse analitico del filone
  - oppure solo support dataset

## Prossimo passo minimo

- eseguire `run all` sui tre `source dataset`
- verificare schema reale e righe utili su `2020-2024`
- fare una prova di join minima
- decidere se passare a:
  - notebook `v0`
  - filtro sui soli comuni con `join_b_ok` e `join_c_ok`
  - prima lettura su costo vs kg vs percentuale RD

## Esito del primo step

Primo gate chiuso:

- i tre endpoint ISPRA reggono davvero su `2020-2024`
- i tre `source dataset` producono `raw`, `clean` e `mart`
- il filone ha un primo `compose` minimo su `codice_comune_istat x anno`

Copertura join del primo compose:

- `2020`: `4397` comuni con join pieno `A + B + C` su `7628`
- `2021`: `4659` comuni con join pieno `A + B + C` su `7618`
- `2022`: `5454` comuni con join pieno `A + B + C` su `7631`
- `2023`: `6250` comuni con join pieno `A + B + C` su `7669`
- `2024`: `6477` comuni con join pieno `A + B + C` su `7671`

Interpretazione iniziale:

- il cross regge tecnicamente
- la copertura dei dataset costi non e` ancora totale sul perimetro RU base
- il primo notebook dovra distinguere bene:
  - perimetro completo RU
  - perimetro ridotto con join `A + B + C`
