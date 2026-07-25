# ANAC — Mapping CIG → CUP

**Dataset**: `anac_cup`
**Fonte**: ANAC — Autorità Nazionale Anticorruzione, [dati.anticorruzione.it](https://dati.anticorruzione.it/opendata/dataset/cup)
**Licenza**: CC BY-SA 4.0

## Contenuto

Bridge table che associa ogni CIG (Codice Identificativo Gara) al suo CUP (Codice Unico di Progetto).
Due sole colonne: `CIG` e `CUP`. Consente di collegare l'universo ANAC (appalti) con l'universo progetti (OpenCUP, MOP, PNRR).

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | Codice Identificativo Gara (10 caratteri) |
| `cup` | VARCHAR | Codice Unico di Progetto (15 caratteri) |

## Copertura

| Metrica | Valore |
|---|---|
| Righe | ~7.12M |
| CIG distinti | ~7.00M |
| CUP distinti | ~1.54M |
| Peso CSV zippato | ~81 MB |
| Periodo | 2000-2026 |
