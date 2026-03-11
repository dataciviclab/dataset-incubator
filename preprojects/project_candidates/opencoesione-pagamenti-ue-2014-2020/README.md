# opencoesione-pagamenti-ue-2014-2020

## Domanda

Per regione e per tema, quanta parte dei fondi UE del ciclo 2014-2020 e stata effettivamente pagata?

## Dataset

Fonte principale:

- OpenCoesione `Progetti con tracciato esteso`

Perimetro iniziale volutamente stretto:

- ciclo: `2014-2020`
- filtro: `FINANZ_UE > 0`
- granularita di lettura: `regione x tema sintetico`
- metriche chiave:
  - `finanz_ue_tot`
  - `tot_pagamenti_tot`
  - `ratio_spesa`

## Stato attuale

Il candidato nasce da un intake tecnico fatto in `datasets-testing` sul tracciato esteso OpenCoesione.

Run verificati nel repo:

- `raw` OK
- `clean` OK
- `mart` OK
- notebook `v0` presente

Problemi gia identificati:

- file grande: ZIP ~249 MB, CSV decompresso ~4.4 GB
- colonne finanziarie con virgola decimale italiana
- ciclo `2021-2027` ancora troppo immaturo per una prima lettura
- il perimetro regionale va stretto a regioni italiane vere
  - esclusi `AMBITO NAZIONALE`
  - esclusi aggregati multi-regione
  - escluso `PAESI EUROPEI`

Punti buoni:

- domanda civica forte
- copertura territoriale nazionale
- campi regione / tema / ciclo / pagamenti gia presenti
- output minimo leggibile senza dover costruire una pipeline enorme
- il file reale ha retto in `utf-8` nel run corrente

## Output minimo atteso

Tabella `regione x tema` con:

- `finanz_ue_tot`
- `tot_pagamenti_tot`
- `ratio_spesa`
- `n_progetti`

Primi segnali emersi:

- il mart finale ha `220` righe `regione x tema`
- compaiono ratio di spesa molto bassi in alcune combinazioni specifiche
- primi casi da guardare: `Molise / Trasporti e mobilita`, `Molise / Ambiente`, `Sicilia / Cultura e turismo`

## Domande complementari

- quali regioni del Sud mostrano i ratio di spesa piu bassi?
- temi come `Ambiente` e `Reti digitali` hanno ratio sistematicamente piu bassi?
- il gap pagato/assegnato e diffuso o concentrato in pochi temi?

## Criterio di promozione

- [ ] raw eseguibile
- [ ] clean eseguibile sul ciclo `2014-2020`
- [ ] mart leggibile a livello `regione x tema`
- [x] primo notebook o query v0 con lettura prudente
- [ ] decisione se entra in `dataciviclab/preanalysis`
