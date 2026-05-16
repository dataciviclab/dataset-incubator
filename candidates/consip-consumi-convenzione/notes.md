# Notes

## Tecnico

### Fonte
- Portale CKAN: `https://dati.consip.it`
- Dataset CKAN: `dataset-consumi-generati-tramite-ordini-diretti-di-acquisto-in-convenzione`
- URL pattern: `https://dati.consip.it/download/dataset/consumi-in-convenzione-{year}.csv`
- Tracciato record (schema): `https://dati.consip.it/tracciato/tracciato-record-consumi-generati-tramite-ordini-diretti-di-acquisto-in-convenzione.xlsx`

### File CSV
- 12 colonne, header con `#` nel nome della prima colonna (`#Anno_Riferimento`)
- Delimitatore: `,`
- Decimali: virgola (es. `3841,24`). Valori numerici quotati con `"`
- Encoding: utf-8
- Schema identico per tutti gli anni (2023, 2024, 2025)

### Anni
| Anno file | Righe dati | Anno riferimento nei dati | Note |
|---|---|---|---|
| 2023 | 8.085 | 2023 | OK |
| 2024 | 8.048 | 2024 | OK |
| 2025 | 7.115 | 2025 | OK |
| 2026 | 7.115 | 2025 | DUPLICATO di 2025, ignorare |

### Anomalie note
- Il file `consumi-in-convenzione-2026.csv` è identico al 2025 (stesso contenuto, stessi dati con `#Anno_Riferimento=2025`). Non usare come anno separato.
- La colonna `#Anno_Riferimento` inizia con `#`, va quotata in SQL come `"#Anno_Riferimento"`.
- I valori numerici con virgola decimale sono quotati nel CSV, quindi letti come VARCHAR. La clean.sql converte via `replace(..., ',', '.')`.

## Analitico

### Domanda guida
Geografia della spesa delle PA in convenzione Consip per utility (energia, gas, carburanti).

### Dimensioni analitiche
- Temporale: anno (2023-2025)
- Geografica PA: regione, provincia, sigla provincia
- Geografica fornitore: regione
- Tipologia PA: amministrazione (Comune, ASL, Università, etc.)
- Prodotto: convenzione, lotto

### Metriche
- Valore economico consumi (€)
- Numero ordini
- Numero PA coinvolte
- Numero punti di prelievo

## Cautele

- La serie storica è omogenea su tutti gli anni? Sì, schema identico per 2023-2025.
- Ci sono discontinuità dichiarate dalla fonte? Non dichiarate.
- I valori nulli sono zero reale o dato mancante? Verificare: la colonna `Valore_economico_consumi` non dovrebbe avere null (è il dato principale). Se presente, probabilmente è dato mancante.
- `Valore_economico_consumi` usa virgola come separatore decimale. La conversione è corretta.
- I dati sono aggregati per coppia PA-convenzione-lotto, non transazionali. I valori come `numero_ordini_con_consumi` e `n_pa_con_consumi` sono conteggi aggregati.
