# Notes

## Tecnico

- CSV INPS usa `;` come delimitatore, `.` per valori mancanti/zeri campi
- La colonna `settore_specifiche` contiene sia sotto-settori reali che righe di totale parziale (`Totale`)
  → filtrarle via nel clean per avere solo il dettaglio in input
- Encoding: UTF-8 con caratteri escape (`_`) per spazi e caratteri speciali
- Anni presenti nella serie: 2005–2024 (20 anni)
- Il file è interamente annuale, non ha granularità mensile/provinciale nella serie storica annuale

## Analitico

- La CIG Ordinaria domina negli anni normali; la Straordinaria sale in crisi (2008-2012)
- La CIGS (solidarietà) ha un pattern proprio, meno presente nella serie lunga
- La pandemia 2020-2021 dovrebbe risultare come spike elevato sulla CIGO
- Le righe "Totale" per settore danno un utile sanity check (somma = totale)

## Cautele

- La serie è omogenea dal 2005 in poi. Prima del 2005 i confini settoriali cambiano.
- ATECO/INPS codification: la classificazione INPS non è ATECO verbatim, serve cautela nei join con altre fonti
- I punti `.` come valori nulli vanno convertiti a NULL esplicitamente per non falsare le medie
- La somma di operai + impiegati può non corrispondere al totale per arrotondamenti dichiarati dalla fonte
