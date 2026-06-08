## Tecnico
- Encoding: latin-1 (tutti e 4 i file)
- Delimiter: ";"
- Header: identico su tutti e 4 gli anni (23 colonne)
- File 2020 e 2021 in `/sites/default/files/imported/`
- File 2022 e 2023 in `/sites/default/files/YYYY-MM/`
- Dimensione: ~2,8 MB/anno, cumulativo ~11 MB

## Analitico
- Domanda guida: trend posti letto Terapia Intensiva e altre discipline chiave
- Possibile analisi: confronto Nord/Sud, distribuzione per tipo struttura

## Cautele
- La serie storica è omogenea su tutti gli anni? ✅ header identico verificato su 2020, 2021, 2023
- Ci sono discontinuità dichiarate dalla fonte? Da verificare nei dizionari PDF
- I valori nulli sono zero reale o dato mancante? Da verificare
- File 2020 e 2021 sono "imported" — verificare encoding esatto
- Separatore delle migliaia? I numeri sembrano senza separatore (es. 108 è 108)
