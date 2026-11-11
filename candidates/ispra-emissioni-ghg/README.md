# ispra-emissioni-ghg — Emissioni GHG da processi energetici per settore (1990-2024)

**Dataset**: emissioni di gas serra (CO₂ equivalente) da processi energetici in Italia, per settore economico. Dati ISPRA — Inventario Nazionale delle Emissioni (UNFCCC/EEA).

**Fonte**: ISPRA — Indicatori Ambientali
https://indicatoriambientali.isprambiente.it/it/energia/emissioni-di-gas-serra-da-processi-energetici-settore-economico

**Issue**: [#491](https://github.com/dataciviclab/dataset-incubator/issues/491)

## Domanda guida

Come si sono evolute le emissioni di gas serra da processi energetici in Italia per settore dal 1990 a oggi? Stiamo decarbonizzando, settore per settore, rispetto agli obiettivi Fit for 55 e neutralità climatica 2050?

## Dataset

- **Copertura**: 1990-2024 (35 anni)
- **Granularità**: nazionale, 4 settori energetici
- **Settori**: Industrie energetiche, Industrie manifatturiere, Terziario e Residenziale + Agricoltura e Pesca (colonna storica `residenziale_e_servizi`), Trasporti
- **Metrica**: Mt CO₂ equivalente (tutti i gas serra pesati)
- **Colonne**: 6 (anno, 4 settori, totale)
- **Fonte**: ISPRA — Inventario Nazionale, dati comunicati a UNFCCC, metodologia IPCC
- **Join key**: anno (per join con Terna, AIFA, altri dataset annuali)

## Perché vale la pena

- **Gap totale colmato**: primo dataset su emissioni/clima nel catalogo Lab
- **Tema caldissimo**: decarbonizzazione, Fit for 55, PNIEC, neutralità climatica
- **Fonte autorevole**: ISPRA Inventario Nazionale, metodologia IPCC
- **Serie storica lunga**: 35 anni di trend analysis
- **Sforzo intake minimo**: XLS già quasi-tidy

## Output minimo atteso

- Dataset clean `ispra_emissioni_ghg_clean.parquet` con schema: anno, settori, totale
- Mart con serie storica per settore
- Notebook v0: trend emissioni per settore 1990-2024

## Criterio di promozione

- Run full passato (RAW→CLEAN→MART), readiness 5/5
- 35 anni, 6 colonne, dati coerenti col trend atteso

## Limitazioni note

- **Solo nazionali**: non c'è disaggregazione regionale in questo indicatore
- **Solo processi energetici**: ~80% delle emissioni totali italiane. Non include agricoltura, rifiuti, processi industriali non energetici, F-gas
- **Fonte XLSX**: il file originale è XLSX, convertito in CSV via script `preprocess.py`
- **Header su due righe**: la riga 1 contiene l'unità di misura (MtCO2 equivalente) — rimossa nel preprocessing
- **Serie revisionata**: ISPRA ricalcola l'intera serie a ogni rilascio; i valori storici possono cambiare
- **Terza colonna**: dal rilascio 2026 è "Terziario e Residenziale + Agricoltura e Pesca" (perimetro più ampio del vecchio "Residenziale e servizi")

## Stato

- ✅ Run full passato (RAW→CLEAN→MART)
- ✅ 35 righe, 6 colonne (1990-2024)
- ✅ Mart: 145 righe (140 settori×anno + 5 trend)
- ⏳ Da pubblicare su explorer

## Prossimo passo

- Notebook v0: trend emissioni per settore
- Analisi pubblica in `dataciviclab/analisi/`
