# camera-incarichi

**Domanda guida:** Quali ruoli hanno ricoperto i deputati nei gruppi parlamentari, in quali legislature e con quali date?

**Fonte:** Camera dei Deputati — OpenData SPARQL (`https://dati.camera.it/sparql`)
**Dataset:** `ocd:incarico` (3.096 incarichi nei gruppi parlamentari)
**Licenza:** CC BY 3.0

## Perché vale la pena

Gli incarichi nei gruppi parlamentari (presidenze, vicepresidenze, capigruppo, rappresentanti...) aggiungono la dimensione "cosa ha fatto" al "chi è" dei deputati. Incrociabile con `camera_deputati_legislature` (via codice deputato) e con `camera_votazioni_sparql` (comportamento di voto per gruppo).

## Output minimo atteso

- `mart_ruoli_legislatura`: incarichi/gruppi/deputati per legislatura
- `mart_top_deputati`: deputati con più incarichi e ruoli distinti

## Criterio di promozione

Promuovere quando: (1) la distribuzione degli incarichi per legislatura è verificata e citabile; (2) il join con `camera_deputati_legislature` funziona sul codice deputato; (3) almeno una domanda civica usa i dati (es. turnover dei ruoli nei gruppi).

## Stato / prossimo passo

- **Stato**: support a standard v1 (2026-08-03) — 2 mart serie
- **Prossimo passo**: verifica run, poi estensione `camera_deputati_legislature` (paginazione per legislatura + anagrafica)
