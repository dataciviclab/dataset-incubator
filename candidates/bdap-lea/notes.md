# Notes

## Tecnico

- dump CSV verificato via HTTPS sul datastore CKAN:
  `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/d598ebd9-949d-4214-bb33-cd9c1be08f15.csv`
- header reale verificato localmente
- delimitatore `;`
- encoding da gestire esplicitamente nel `clean.read`
- `toolkit inspect paths` OK: `effective_root` risolve a `dataset-incubator/out`
- run aggiornato 2026-05-25:
  - clean: 23.595 righe (filtro voci totali `codice_voce_contabile NOT IN ('19999','29999','39999','48888','49999')`)
  - mart: 22.180 righe (filtro voci totali + `codice_ente_ssn <> '000'`)
- fix double-counting 2026-05-25: le voci di totale (19999,29999,39999,48888,49999) duplicavano gli importi delle voci di dettaglio.
  SUM importo_totale pulito da 1.410 mld € a 748 mld € (-47%).

## Analitico

- il v0 parte sul solo `2024`
- perimetro analitico: esclude `codice_ente_ssn = '000'` (filtro in mart)
- la domanda guida resta sulla prevenzione collettiva, ma il candidate lascia anche altre voci contabili per letture successive

## Cautele

- i dati sono contabili di spesa, non misurano esiti di salute
- gli enti `000` sono aggregazioni regionali e causano double-counting se sommati ai singoli enti
- alcuni codici voce sono aggregati di sezione e vanno trattati con prudenza nelle letture successive
- la serie storica 2012-2024 esiste, ma non entra nel primo ciclo tecnico
- CI usa `toolkit run full --smoke` (toolkit v1.13.2+) — sample-bytes + sample-rows + skip min_rows
