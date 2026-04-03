# MIM alunni per corso ed età

## Domanda

- Quali territori mostrano il calo più forte di iscritti nelle scuole primarie statali?

## Dataset

- fonte principale: MIM `Alunni per corso ed età`
- support dataset: `SCUANAGRAFESTAT`
- file v0 intake: `ALUCORSOETASTA20242520250831.csv`
- URL verificato: `https://dati.istruzione.it/opendata/opendata/catalogo/elements1/ALUCORSOETASTA20242520250831.csv`
- licenza dichiarata: `IODL 2.0`

## Perché vale la pena incubarlo

- granularità a livello `CODICESCUOLA`
- forte leggibilità civica sul calo iscrizioni
- il nuovo blocco `support:` del toolkit rende dichiarativo il join con l'anagrafica scuole

## Output minimo atteso

- raw: download CSV diretto del file alunni 2024/25
- clean: tabella normalizzata con `CODICESCUOLA`, ordine, anno di corso, fascia età e numero alunni
- mart: aggregato territoriale sulle scuole primarie statali tramite join con anagrafica
- notebook v0 minimo per sanity check del mart

## Stato

- intake
- perimetro v0 ristretto a `2024/25`
- focus iniziale sulle sole primarie

Issue collegata:
- `dataset-incubator#106`

## Prossimo passo

- verificare run reale candidate + support dataset
- estendere poi il candidate a una finestra multi-anno se il naming MIM regge bene nel contratto
