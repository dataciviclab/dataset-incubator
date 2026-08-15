# Notes — bdap-pagamenti-stato

## Fonte

- **Fonte**: MEF / OpenBDAP — "Pagamenti Bilancio dello Stato per Amministrazione Missione Categoria Economica"
- **Portale CKAN**: `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3`
- **Tipo**: **CONSUNTIVO** dei pagamenti dello Stato (dati osservati l'anno successivo)
- **Copertura**: consuntivi annuali 2014-2025 (12 anni)
- **Granularità**: 1 riga = Amministrazione × Missione × Categoria economica × anno

## Perché questo dataset

È il **consuntivo** dei pagamenti dello Stato, complementare a `bdap_spese_stato`
(previsioni). È il dato **reale pagato**, che completa il triangolo:
- previsione (bdap_spese_stato)
- stima interessi (OCPI)
- **consuntivo (questo)**

## Struttura

16 colonne:
- dimensioni: `esercizio_finanziario`, `codice_stp` (codice ministero), `amministrazione`,
  `codice_missione`, `missione`, `codice_categoria`, `categoria`
- metriche per canale di pagamento: `op_erario`, `op_tesoreria`, `op_esterno`,
  `oa_tesoreria`, `oa_spesa_funz_deleg`, `rsf_stipendi`, `rsf_altro`,
  `note_imputazione`, `totale_pagato`

Numeri in formato standard (punto decimale), header con `;`.

## Missione "Debito pubblico" (codice 034, Ministero Economia)

Categorie rilevanti (verificate consuntivo 2024):
- `09` — INTERESSI PASSIVI E ALTRI ONERI FINANZIARI (82,1 mld nel 2024)
- `61` — RIMBORSO PASSIVITA' FINANZIARIE (282,6 mld nel 2024)
- `31` — ACQUISIZIONI DI ATTIVITA' FINANZIARIE (3,0 mld)
- `02` — CONSUMI INTERMEDI (0,9 mld)

## Verifica di coerenza

Consuntivo 2024 interessi missione debito = **82,1 mld** vs OCPI 2024 = **85,9 mld**
→ differenza 3,8 mld (4%). Il sistema debito-pubblico-intelligence usa questo
per il caso reconcile 6 (costo consuntivo vs stima).

## Review standard candidate (2026-08-15)

Allineato a `candidate-standard.md` v1:
- `primary_key` clean dichiarato e verificato unico:
  `(esercizio_finanziario, codice_stp, codice_missione, codice_categoria)` (548=548)
- `primary_key` mart dichiarato e verificato unico:
  `(esercizio_finanziario, amministrazione, missione, categoria)` (548=548)
- `clean.required_columns` e `mart.table_rules.required_columns` presenti
- `read.source: config_only` motivato: CSV con colonna vuota finale, serve il
  mapping colonne esplicito (forma canonica §2.3)
- `toolkit run` ok su tutti i 12 anni; `validate_candidate_structure.py` senza warning

## Caveat tecnici

- **package_show via slug fallisce** su OpenBDAP: va usato l'**UUID** del package
- **http dà timeout**: necessario HTTPS (il plugin ckan del toolkit forza HTTPS)
- I resource CSV non hanno `datastore_active=True` → il plugin usa l'URL diretto (dump), che funziona
- Server lento: timeout alto necessario (60-120s)
- Consuntivi annuali cumulativi per definizione

## Stato

- intake: da collegare (issue dataset-incubator)
- in bootstrap
