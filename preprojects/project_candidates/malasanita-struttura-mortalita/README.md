# malasanita-struttura-mortalita

## Domanda

Le regioni con meno personale sanitario hanno tassi di mortalità evitabile più alti?

## Dataset

Anno pivot: **2022** — unico anno di sovrapposizione completa tra le fonti.

| ID | Fonte | Copertura | Formato |
|---|---|---|---|
| A | Strutture e attività ASL — dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| B | Reparti strutture di ricovero — dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| C | Strutture ricovero per ASL — dati.salute.gov.it | fino al 2022 | CSV/XLSX |
| D | Mortalità per causa — dati.istat.it | fino al 2022-2023 | ZIP→XLSX |

Fonti di secondo livello (fuori dalla preanalysis finché il nucleo CSV non regge):
- AGENAS/SIMES
- MedMal Marsh

## Perche vale la pena testarlo

- Domanda civica forte e leggibile
- Tutte le fonti del nucleo sono pubbliche e scaricabili
- Combinazione personale sanitario + mortalità evitabile = segnale interpretabile
- Confronto regionale praticabile con anno pivot 2022

## Output minimo atteso

- Confronto regionale personale sanitario / mortalità evitabile per il 2022
- Mappa o tabella regioni con indicatori chiave
- Nota metodologica su gap temporale Ministero e scelte di perimetro

## Criterio di promozione

- CSV A/B/C/D scaricabili e leggibili
- Join regionale stabile su codice regione ISTAT
- Almeno un segnale interpretabile emerge dall'incrocio

## Stato

active — verifica fonti completata, avvio task tecnico su fonte D

## Decisioni metodologiche prese (Discussion #99 con @Gabrymi93)

- AGENAS/SIMES e MedMal Marsh → secondo livello, fuori dalla preanalysis finché il nucleo CSV non regge
- Emilia-Romagna → benchmark metodologico opzionale, esclusa dall'analisi principale
- Gap temporale dati Ministero (fermati al 2022) → parte della narrativa, documentare esplicitamente in nota metodologica

## Prossimo passo

Testare il path nativo della fonte D (`ZIP extractor + clean XLSX`) in incubator privato; se instabile, applicare fallback documentato (`pre-ingest` + `local_file`).
