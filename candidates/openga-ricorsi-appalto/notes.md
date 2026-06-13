## Tecnico

- Source type: `ckan` (resource_name pattern `"CDS - Ricorsi pervenuti in materia d'appalto - {year}"`)
- 2023: risorsa DataStore con colonna `_id` extra — gestita con columns espliciti in clean.read
- 2024-2026: risorse upload standard, 24 colonne
- Granularità: singolo ricorso (record-level)
- Topic: giustizia
- Frequenza mensile: i dati vengono aggiornati ogni mese dalla fonte

## Analitico

- Colonna `ANNO_DEPOSITO_RICORSO`: anno effettivo di deposito (non coincide necessariamente con l'anno file)
- `IMPORTO_COMPLESSIVO_GARA` e `IMPORTO_LOTTO`: valori con `,` come separatore decimale, gestiti in clean
- `CLASSIFICAZIONE_RICORSO`: tassonomia che include "APPALTI SANITÀ", "PIANO NAZIONALE DI RIPRESA E RESILIENZA (PNRR)", "APPALTI PUBBLICI DI SERVIZI/LAVORI", ecc.
- `CODICE_CIG`: presente per la maggior parte dei ricorsi, permette join con dataset ANAC
- Notevole la presenza di ricorsi PNRR già dal 2023
- Solo Consiglio di Stato (II grado), non include i ricorsi di I grado (TAR)

## Cautele

- La serie storica 2023 è in formato DataStore dump (con `_id`), anni successivi in upload standard — i dati sono omogenei ma la struttura raw differisce
- I campi `CODICE_CIG`, `LUOGO_ISTAT`, `PROVINCIA` hanno valori nulli per alcuni ricorsi (non tutti i ricorsi hanno una gara associata)
- `DATA_SCADENZA_OFFERTA` e `DATA_PUBBLICAZIONE` talvolta vuote
- L'`ANNO_DEPOSITO_RICORSO` nei file 2024+ può includere ricorsi depositati in anni precedenti (il file 2024 contiene ricorsi con anno deposito = 2009)
- I valori nulli in `IMPORTO_COMPLESSIVO_GARA` sono assenza della gara, non zero
- **Dati economici/geografici differiti**: per gli anni più recenti (2025-2026) `IMPORTO_COMPLESSIVO_GARA`, `IMPORTO_LOTTO`, `PROVINCIA` e `LUOGO_ISTAT` sono quasi sempre nulli. I ricorsi sono depositati ma i dettagli della gara vengono popolati successivamente. Il dataset è più informativo per l'anno -2 rispetto all'anno corrente (es. nel 2026 i dati 2024 sono i più completi: 151/905 con importo, 54/905 con provincia)
- **Anno 2023**: solo 22 ricorsi (dato parziale, probabilmente solo ricorsi ancora pendenti al momento della prima pubblicazione del dataset a dicembre 2024)
