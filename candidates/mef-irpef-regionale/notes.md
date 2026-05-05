# Note tecniche — mef-irpef-regionale

## Fonte

MEF Dipartimento Finanze — Open Data IRPEF:
- Primary: `REG_tipo_reddito_{year}.csv`
- Secondary: `REG_calcolo_irpef_{year}.csv`, `REG_bonus_irpef_{year}.csv`

URL base: `https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/`

## Copertura temporale

2017–2025 (9 anni di dichiarazione). I file pre-2017 restituiscono 404.

## Struttura raw

CSV con `;` delimiter, encoding `utf-8`.
- Header riga 1 (da skip)
- Dati: 441 righe teoriche per anno = 21 regioni × 21 classi di reddito
- Colonna 1: "Classi di reddito complessivo in euro"
- Colonna 2: "Regione"
- Colonne 3–64: coppie frequenza/ammontare per ogni tipologia di reddito

## Schema clean (da definire post-run)

52 colonne dichiarate per REG_tipo_reddito. Verificare con `toolkit_raw_profile`.

## Schema clean

42 colonne dichiarate in dataset.yml, di cui 39 per tipologie di reddito (coppie freq+eur).

## Caveat

- **34 classi vs 21**: il dataset MEF REG ha 34 classi di reddito (non 21 come nell'issue #253). Il mart.sql copre le 21 più diffuse — classe `ELSE 99` per le altre 13.
- **Contributi nulli**: le celle vuote indicano valori nulli (NON zero reale). Gestiti con NULLIF + regexp_replace per separatori italiani.
- **Dimensione sesso assente**: l'issue #253 menzionava "per classe e sesso". I file REG_tipo_reddito non hanno breakdown per sesso — la dimensione sesso è disponibile solo nei file `sesso_*` del portale MEF (stesso source_id `mef_irpef`). Per ora la v1 è solo regione × classe × anno. L'analisi di genere richiede un candidate separato.

## Note di ingest / clean

- Il toolkit supporta `{year}` nella clean.sql — il template renderer lo sostituisce prima dell'esecuzione. Usare sempre `{year}::INTEGER` per la colonna `anno_di_imposta`, mai valori hardcoded.
- 34 classi di reddito nel MEF REG (vs 21 dichiarate nell'issue) — il mart.sql copre solo le 21 più diffuse, classe `ELSE 99` per le altre.
- Filtro `Mancante/errata` gia nel WHERE della clean.sql.

## Status

Pipeline OK per 2024, 2023, 2025. Multi-anno confermato. PR ready.