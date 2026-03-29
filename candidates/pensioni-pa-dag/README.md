# Pensioni PA DAG

## Domanda

- Come si distribuisce territorialmente lo stock di pensioni dello Stato gestite dal DAG, e come cambia la composizione tra trattamenti diretti e indiretti/reversibili tra regioni?

## Dataset

- fonte: MEF DAG, sezione open data `Tipo Pensione`
- pagina fonte: `https://datipensioni.mef.gov.it/datipensioni/download`
- download riproducibile: `POST https://datipensioni.mef.gov.it/datipensioni/downloadFile`
- file cumulativo usato nel v0: `Dati_Tipo_Pensione_totale.csv`
- licenza dichiarata dalla fonte: `CC BY 4.0`
- caveat chiave: il toolkit non ha ancora un source type `http_post_file`, quindi il candidate usa uno script locale di staging in `scripts/download_raw.py`

## Perche vale la pena testarlo

- fonte pubblica poco usata e distinta dal perimetro INPS
- granularita utile: anno, mese, territorio, tipo trattamento, microqualifica
- buon complemento del filone `dipendenti-pubblici` sul lato passivo del settore pubblico
- domanda civica leggibile su concentrazione territoriale e composizione dei trattamenti

## Output minimo atteso

- raw staged via script dedicato e letto come `local_file`
- clean 2024 filtrato su `DIRETTA` e `INDIRETTA/REVERSIBILE`
- mart regionale su snapshot di dicembre 2024
- base pronta per notebook v0 o analisi successiva

## Criterio di promozione

- perimetro dichiarato con chiarezza: pensioni DAG, non totale pensioni italiane
- snapshot regionale dicembre 2024 leggibile e difendibile
- rischio tecnico della fonte POST documentato in modo esplicito

## Stato

- intake

Issue collegata:
- `dataset-incubator#96`

## Prossimo passo

- valutare se il pattern merita un source type `http_post_file` nel toolkit oppure resta staging via script locale
