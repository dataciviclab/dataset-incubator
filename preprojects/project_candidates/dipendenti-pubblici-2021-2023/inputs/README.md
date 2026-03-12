# Inputs locali opzionali

Questa cartella non versione i CSV sorgente e non e necessaria per il run normale.

Usarla solo come fallback locale se il feed pubblico BDAP/RGS cambia o smette di rispondere.

In quel caso, mettere qui:

- `dipendenti_pubblici_2021.csv`
- `dipendenti_pubblici_2022.csv`
- `dipendenti_pubblici_2023.csv`

Origine pratica del caso locale:

- materiale locale gia usato in `datasets-testing/preprojects/multi_year_schema/case_15_dipendenti_pubblici_2021_2023`

Nota:

- i file possono richiedere lettura `cp1252`
- il preproject usa di default il download HTTP della fonte pubblica
