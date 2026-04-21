# mur-contribuzione-universitaria

Candidate per la contribuzione universitaria MUR: gettito, esoneri e interventi per ateneo (2009-2024).

## Stato

`intake` — in fase di verifica tecnica iniziale.

## Issue

- `dataciviclab/dataset-incubator#150`

## Domanda guida

Come varia il gettito della contribuzione studentesca tra atenei e tipologia di corso? Quali atenei hanno la quota più alta di esoneri totali rispetto al totale iscritti?

## Fonte

- **MUR – Contribuzione e interventi atenei**
- Portale: https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei
- Licenza: IODL-2.0 (Pubblico Dominio)
- Formato: CSV, semicolon-separated, encoding latin-1

## Perché vale la pena incubarlo

- Tema ad alta domanda civica: costo dell'università, accesso e diritto allo studio
- Dati amministrativi ufficiali, comparabili tra atenei (~80+)
- Aggiornamento annuale, formato CSV accessibile
- Il gettito per tipologia di corso permette confronti trasversali

## Output minimo atteso

- Mart gettito per ateneo e tipologia di corso (A.A. 2023/24)
- Notebook v0 di validazione

## Cautele

- Encoding latin-1: serve configurazione esplicita nella read
- Un file per anno — per serie storica servono più file da unire
- Dataset DSU regionale è su CKAN separato (fuori perimetro v0)
- Granularità per ateneo, non per singolo corso di laurea

## Prossimo passo

Eseguire toolkit run raw → clean → mart e verificare che il parse dell'encoding latin-1 e del delimitatore `;` sia corretto.