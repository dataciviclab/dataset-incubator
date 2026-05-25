# Notes

## Tecnico

- dump CSV verificato via HTTPS sul datastore CKAN:
  `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/d598ebd9-949d-4214-bb33-cd9c1be08f15.csv`
- header reale verificato localmente
- delimitatore `;`
- encoding da gestire esplicitamente nel `clean.read`
- `toolkit inspect paths` OK: `effective_root` risolve a `dataset-incubator/out`
- run aggiornato 2026-05-25:
  - clean: 20.036 righe (filtro voci totali + `codice_ente_ssn NOT IN ('000','999')`)
  - mart: 20.036 righe (stesso perimetro)
- fix double-counting voci totali (2026-05-25): le voci 19999,29999,39999,48888,49999 duplicavano gli importi dettaglio.
- fix double-counting enti 999 (2026-05-25): gli enti regione (999) andavano esclusi come i 000.
  Pulitura finale: da 1.410 mld € (tutto incluso) → 748 mld (senza totali) → 738 mld (senza 000) → 396 mld (senza 999).

## Analitico

- il v0 parte sul solo `2024`
- perimetro analitico: esclude `codice_ente_ssn IN ('000', '999')`
- la domanda guida resta sulla prevenzione collettiva, ma il candidate lascia anche altre voci contabili per letture successive

## Cautele

- i dati sono contabili di spesa, non misurano esiti di salute
- gli enti `000` (aggregazioni regionali) e `999` (enti regione) causano double-counting se sommati agli enti ASL/ATS
- `prestazioni_sanitarie` (~€166 mld) sono transazioni inter-ente (mobilità sanitaria) — ogni prestazione è contata sia da chi paga sia da chi eroga
- alcuni codici voce sono aggregati di sezione e vanno trattati con prudenza nelle letture successive
- la serie storica 2012-2024 esiste, ma non entra nel primo ciclo tecnico
