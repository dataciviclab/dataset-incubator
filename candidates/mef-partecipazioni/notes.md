## Note tecniche

### Encoding e parsing
- File: CSV con delimitatore `;`, encoding `latin-1`
- Header: riga 1, colonne con spazi e caratteri speciali
- 93 colonne totali per anno — schema stabile a 84 colonne comuni

### Clean.sql — scelte
- 84 colonne selezionate (di 93 totali per anno) — solo colonne comuni a tutti gli anni
- 9 colonne anno-specifiche escluse: Fatturato N, Risultato d'esercizio N, Partecipata bilancio N approvato
- Nessun filtro WHERE — raw faithful, nessuna riga esclusa
- importo_impegnato_servizio_5 è castato VARCHAR (vs BIGINT per 1-4) per anomalia dati: il campo contiene stringhe non numeriche in alcuni anni

### Mart.sql — scelte
- Aggregazione: count partecipazioni, distinct amministrazioni, distinct partecipate
- Raggruppamento: regione, provincia, comune, categoria amministrazione
- Metriche: % perimetro TUSP, % perimetro revisione periodica

### Schema variability

Il portale MEF pubblica dati con schema che varia per anno — le colonne con l'anno nel nome (es. `Fatturato 2021`, `Risultato d'esercizio 2023`) cambiano a seconda dell'anno di rilevazione. Per garantire uno schema clean costante, la clean.sql seleziona solo le 84 colonne presenti in tutti gli anni disponibili.

Anni verificati: 2020, 2021, 2022, 2023. Tutti gli anni con URL dedicato.

## Caveat analitici

- Dato dichiarativo: copertura dipende dall'adempimento
- Serie storica: 4 anni (2020-2023)