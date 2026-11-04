# centri-accoglienza-italia

## Issue
DataCivicLab/dataset-incubator#595

## Fonte
Centri d'Italia (ActionAid Italia + Fondazione Openpolis), CC-BY 4.0.
File unico CSV multi-anno (2018-2024), **uno snapshot per anno al 31/12**.

## Tecnico

- Encoding: UTF-8, delim: virgola, decimale: punto (es. 22.77)
- 47.419 righe raw, 29 colonne → **47.213 dopo la dedup** delle 206 righe esatte
  duplicate della fonte (concentrate nel 2023-24)
- **Granularità**: centro × **convenzione** in una rilevazione annuale. Lo stesso
  `centro_id` compare più volte (più contratti con capienza e date diverse):
  il mart conta `COUNT(DISTINCT centro_id)` come numero di centri e
  `SUM(capienza)` su tutte le convenzioni.
- Geografia con codici ISTAT a tutti i livelli (comune, provincia, regione)

## Analitico

- **CAS ADULTI** è la tipologia dominante (47.007 righe su 47.419); CPA (72),
  HOTSPOT (35) e CAS MINORI (305) sono marginali.
- `costo_giornaliero_per_ospite`: ~26-35 €/giorno (media 35 nel 2018, 26-30 dal 2020).
- **CAS al Nord, SAI al Sud**: nel 2024 la capienza CAS è massima in Lombardia
  (14.679), Lazio (9.934), Emilia-Romagna (9.874), Piemonte (9.868); pro capite
  gli estremi sono Friuli/Basilicata 3,42 e Puglia 0,77 posti/1.000 ab.
- **Sovraffollamento** (convenzioni con presenze > capienza): 6,2% (2018) → 12,2%
  (2022) → **22,8% (2023)** → 16,2% (2024).
- Capacità CAS attiva in calo dal 2018 (133.590 posti) al 2021 (62.926), poi
  risalita a 106.439 nel 2024.

## Cautele

- `capienza = 0` in 1.434 righe (2020) e 1.129 (2021); `capienza` NULL in 13 (2021).
- `costo_giornaliero_per_ospite` NULL in 445 righe (2021) e 552 (2022).
- `presenze_giornaliere` può essere NULL.
- SAI/SIPROIMI non sono in questo CSV (file separati).
- `tipologia_centro` ha varianti testuali (es. "CAS ADULTI", "CAS ADULTI UOMINI").
- Il file bandi ANAC non è accessibile (Access Denied).
