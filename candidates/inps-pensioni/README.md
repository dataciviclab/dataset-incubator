# INPS pensioni per importo, sesso e territorio

## Domanda

- Quante pensioni sotto i 500 euro si osservano per regione, sesso e classe di età, e come cambia la loro quota tra 2017 e 2024?

## Dataset

- fonte: INPS open data, dataset `6002`
- pagina fonte: `https://www.inps.it/it/it/dati-e-bilanci/open-data/scarica-gli-open-data/dettaglio-opendata.opendata.2024.08.numero-totale-pensioni-divise-per-anno,-sesso,-regione,-area-geografica,-tipo-di-gestione,-classe-di-importo,-classe-di-eta-e-categoria---trimestrale.html`
- download riproducibile: `https://www.inps.it/content/dam/inps-site/opendata/2024/08/dataset_6002.csv`
- licenza dichiarata: `IODL v2.0`
- copertura dichiarata nel file: serie trimestrale 2017-2024

## Perché vale la pena incubarlo

- fonte pubblica ad alta leggibilità civica
- granularità territoriale e demografica utile per un v0 difendibile
- buon complemento del filone `pensioni-pa-dag`, che resta distinto per perimetro

## Output minimo atteso

- raw: download diretto del CSV INPS
- clean: tabella normalizzata con anno, trimestre, sesso, classe età, classe importo, regione e numero pensioni
- mart: aggregato regionale per classe importo, sesso e trimestre
- notebook v0 esplorativo su quota pensioni basse e gap territoriale

## Criterio di promozione

- perimetro v0 dichiarato con chiarezza
- trend 2017-2024 leggibile almeno a livello regionale
- eventuali discontinuità tassonomiche nelle classi documentate in modo esplicito

## Stato

- intake

Issue collegata:
- `dataset-incubator#101`

## Prossimo passo

- verificare nel notebook v0 se le classi di importo restano stabili lungo la serie 2017-2024
