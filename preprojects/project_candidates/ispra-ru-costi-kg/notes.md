# Notes - ispra-ru-costi-kg

## Stato tecnico

Branch di lavoro iniziale:

- `feat/ispra-ru-cross-intake`

Stato attuale:

- intake aperto su issue `#30`
- struttura candidate avviata
- nessun `dataset.yml` ancora definito
- nessun `clean` o `mart` ancora portato nel toolkit

## Architettura adottata

Pattern multi-fonte:

- `sources/a_ru_base`
- `sources/b_kg_per_abitante`
- `sources/c_costo_per_abitante`
- `compose/` finale per il cross

Scelta intenzionale:

- non forzare ancora `dataset.yml` o SQL finti
- prima verificare che URL, formato, chiavi e overlap temporale reggano davvero

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

- recuperare e documentare le due tabelle aggiuntive
- verificare chiavi di join e annualita comuni
- fare una prova di join minima
- decidere se passare a:
  - `dataset.yml` + `clean.sql` per i tre source dataset
  - `compose/dataset.yml` + `mart_cross.sql`
  - notebook `v0`
