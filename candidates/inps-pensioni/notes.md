# Notes

## Tecnico

- il candidate usa `http_file` diretto sul CSV pubblico INPS `dataset_6002.csv`
- `years: [2024]` è usato come chiave di snapshot del run; il file contiene già la serie 2017-2024
- il formato CSV evita il parsing del JSON annidato e consente un intake più semplice
- dimensioni incluse nel v0: anno, trimestre, sesso, classe età, classe importo, regione, area geografica

## Analitico

- focus iniziale: pensioni sotto i 500 euro e composizione territoriale
- buon asse secondario: differenze di genere e classi di età
- evitare nel v0 di allargare troppo su `gestione` e `categoria`

## Cautele

- verificare se le classi di importo cambiano semantica nella serie 2017-2024
- tenere separato questo filone da `pensioni-pa-dag`
- non leggere `years: [2024]` come filtro della serie: è solo la chiave di snapshot del candidate
