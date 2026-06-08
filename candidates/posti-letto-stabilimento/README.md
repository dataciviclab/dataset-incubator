# posti-letto-stabilimento

Fonte: Ministero della Salute — Open Data (dati.salute.gov.it)
Dataset: Posti letto per stabilimento ospedaliero e disciplina

Periodo: 2020-2023 (4 annualità, file separati per anno)

## Domanda
Come sono cambiati i posti letto per disciplina e struttura ospedaliera tra il pre-COVID (2020) e il post-COVID (2023)?

## Dataset
- **Copertura**: Italia — tutte le regioni, strutture pubbliche ed equiparate
- **Granularità**: singolo stabilimento ospedaliero × disciplina (reparto)
- **Metriche**: posti letto degenza ordinaria, day hospital, day surgery, totali
- **Colonne**: 23 colonne (anno, regione, azienda, struttura, indirizzo, comune, disciplina, tipo disciplina, n. reparti, posti letto)

## Perché vale la pena testarlo
1. Serie storica pluriennale 2020-2023 (copre anni pandemici)
2. Self-contained — nessuna join esterna per analisi v0
3. Aggiornato: 2023 pubblicato luglio 2025
4. Complementare a `reparti_ricovero` (più ricco ma solo 2022)

## Output minimo atteso
- Dataset clean con 4 annualità unificate
- Mart per regione × disciplina × anno (posti letto aggregati)
- Notebook v0: trend Terapia Intensiva 2020-2023

## Criterio di promozione
- Run full completato su tutti e 4 gli anni
- Almeno una mart con dati sensati (somme non nulle)
- Notebook v0 con analisi esplorativa

## Stato
- intake

## Prossimo passo
- Run full su tutti gli anni
- Validazione dati
- Notebook v0
