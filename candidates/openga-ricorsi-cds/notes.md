## Tecnico

- Fonte: openga (CKAN) — già nel registry SO
- URL risorse: diverse per anno (resource UUID varia)
- 4 anni: 2023, 2024, 2025, 2026 (parziale)
- 4 colonne, ~24 righe per anno intero
- Headers consistenti su tutti gli anni ✅
- CSV header con nomi lowercase con underscore

## Analitico

- I ricorsi pendenti sono una fotografia a fine mese (stock, non flusso)
- Sede 002: probabilmente la sede centrale del CdS (Roma)
- Sede 031: Tar / sezione consultiva (anche se etichettata "CONSIGLIO DI STATO")
- NUMERO_RICORSI_PENDENTI è già un aggregato mensile

## Cautele

- La serie è breve (2023-oggi) — non sufficiente per trend decennali
- 2026 è parziale (solo Q1) — da escludere da confronti annuali
- CODICE_SEDE ha solo 2 valori attualmente, ma potrebbe espandersi
- I valori sono già aggregati per mese-sede — non moltiplicare per mesi
