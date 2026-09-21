## Tecnico

- Fonte: API pubblica non documentata `portale.inpa.gov.it/concorsi-smart/api/concorso-public-area/search-better`
- La lista espone `sedi`, `settori`, `categorie`, `entiRiferimento` come liste di **stringhe**;
  il dettaglio (`GET /concorso-public-area/{id}`) li restituisce come dict con ID e denormalizzazione.
- Endpoint paginato Spring (content/totalPages); `size` max testato: 500
- **Multi-source**: `inpa_open` (OPEN ~2.256 con dettaglio) + `inpa_closed` (CLOSED ~71.000 senza
  dettaglio). `clean.read.mode: all` li unisce con `union_by_name` → colonne dettaglio NULL su CLOSED.
- **Overlap API**: 31 id compaiono sia in OPEN che in CLOSED → dedup nel clean.sql con
  `ROW_NUMBER() OVER (PARTITION BY id ...)` dando priorità a OPEN (ha il dettaglio).
- **Sentinelle `num_posti`**: valori di soli 9 (9999/99999/999999) usati come N/D dagli
  "Elenchi di Idonei" (scorrimento, posti non definiti — es. Provincia di Lecce). Nel clean:
  `regexp_matches(num_posti, '^9+$') AND num_posti > 99 → NULL`. I valori alti reali
  (29.314/30.759 supplenze scolastiche) restano validi. Idem date con anno < 2000.
- **Harvest esplicito** (non a ogni run): genera i CSV in `out/data/raw/inpa_bandi/2026/`.
  Il `dataset.yml` usa `local_file` che legge quei path. Comandi da candidate root:
  - OPEN con dettaglio: `python scripts/harvest_inpa.py raw_input.csv` (~13 min)
  - CLOSED: `python scripts/harvest_inpa.py raw_input_closed.csv --status CLOSED --no-detail` (~17 min)
- Il dettaglio arricchisce OPEN: `company_district_code` (100%), `link_sito_pa` (71%),
  `n_allegati` (96%), `richiede_pagamento` (18%), `pec_obbligatoria` (43%), `is_remote` (8%),
  `salary_min` (4%). `email_referente` mai valorizzato → escluso dal clean.

## Cautele

- **API non pubblicata né documentata**: nessuna garanzia di stabilità; schema può cambiare
  o essere chiusa (backup: `sitemap-bandi.xml` + scrape dettaglio)
- **`num_posti` è sentinella** su alcuni bandi (Elenchi di Idonei, scorrimenti)
- **Multi-sede**: `sedi` è una lista → un bando può avere più regioni/province (join `|` nel CSV)
- **`regione` inPA = sede del bando**, non sempre il banditore (gli enti nazionali compaiono
  in ogni regione) — per confronti regionali usare solo enti locali
- **`linkGazzettaUfficiale` quasi sempre NULL** (0/85 testati): il ponte con la GU non passa da inPA
- Rate limiting non documentato: pause di 0.3s tra pagine nel default dello script

## Decisioni

- Snapshot OPEN (con dettaglio) + storico CLOSED (senza dettaglio) come primo stadio completo;
  dettaglio per tutto il CLOSED rimandato (volume ~7h di chiamate, valore marginale)
- `years: [2026]` = anno di snapshot (non serie storica per-anno)
- `primary_key: [id]` = concorso_id dell'API, univoco per bando

## Bridge con open-conto-annuale (verificato 2026-08-13)

- **Match per nome normalizzato: 84%** (6.215/7.436 enti inPA presenti nel personale CA 2024).
  Normalizzazione: uppercase, rimozione apostrofi/punteggiatura, spazi compatti.
- **`companyDistrictCode` (codice catastale) matcha solo 58%** con `codi_catastale` del seed
  territorio: copre i comuni ma non ministeri/ASL/union. NON è un bridge migliore del nome.
- **`linkGazzettaUfficiale` quasi sempre NULL**: il ponte con la GU non passa da inPA.
- **`codi_fiscale` non esiste nel dettaglio inPA** → join deterministico non ottenibile;
  si usa il nome normalizzato (fuzzy, 84%). Il `company_district_code` aiuta sui comuni.
