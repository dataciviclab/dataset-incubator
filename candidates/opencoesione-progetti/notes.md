# opencoesione-progetti — note

## Fonte

- **Ente**: PCM — Dipartimento Politiche di Coesione / OpenCoesione
- **Portale di riferimento**: dati.gov.it (organization: pcm-opencoesione)
- **File**: `progetti_20260228.parquet` (2.3M righe, 95 colonne)
- **Licenza**: CC BY 4.0
- **Aggiornamento**: 2026-02-28 (data dump)
- **Issue intake**: #440

## Differenze dal vecchio candidato

Il vecchio candidato `opencoesione-pagamenti-ue-2014-2020` usava:
- CSV `progetti_esteso.zip` (~201 colonne, inclusa `DEN_REGIONE`)
- Solo ciclo 2014-2020
- Solo FINANZ_UE > 0
- Formato CSV con virgola italiana → `replace(..., ',', '.')`

Il nuovo candidato usa:
- **Parquet** — nessun parsing CSV, tipi nativi, zero decimal issues
- **Tutti i cicli** (2007-2013, 2014-2020, 2021-2027)
- **Tutti i progetti** (nessun filtro su fonte finanziamento)
- **Macroarea invece di regione** — il parquet ha `OC_MACROAREA` (6 valori: Centro-Nord, Mezzogiorno, Estero, Ambito Nazionale, Altro, Trasversale)

## Decisione di framing

- v0 usa il parquet perché più veloce e pulito
- La granularità geografica è macroarea (non regione) — per analisi regionali servirebbe il CSV esteso o join con `soggetti`
- Il mart aggrega per `ciclo × macroarea × tema` con ratio_spesa e ratio_impegni

## Limiti noti

- `OC_MACROAREA` ha solo 6 valori — nessun dettaglio regionale
- Le date sono INTEGER (formato YYYYMMDD?) — non ancora normalizzate in DATE
- I progetti multi-regione potrebbero essere classificati come "Ambito Nazionale" o "Trasversale"

## Output v0

Tabella `mart_macroarea_tema`:
- `ciclo`, `macroarea`, `tema`
- `n_progetti`
- `finanz_ue_tot`, `finanz_fsc_tot`, `finanz_tot_pub`, `costo_coesione`
- `impegni_tot`, `pagamenti_tot`
- `ratio_spesa` (pagamenti / costo_coesione)
- `ratio_impegni` (impegni / costo_coesione)

## Prossimi passi

- [ ] Run `toolkit run full` per verificare la pipeline
- [ ] Creare notebook v0 con visualizzazione macroarea × tema
- [ ] Valutare se aggiungere `soggetti` e `pagamenti` come support dataset
- [ ] Valutare switch a CSV esteso per granularità regionale in v1
