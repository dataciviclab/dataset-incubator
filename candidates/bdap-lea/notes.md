# Notes

## Tecnico

- dump CSV verificato via HTTPS sul datastore CKAN:
  `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/d598ebd9-949d-4214-bb33-cd9c1be08f15.csv`
- header reale verificato localmente
- delimitatore `;`
- encoding da gestire esplicitamente nel `clean.read`
- `toolkit inspect paths` OK: `effective_root` risolve a `dataset-incubator/out`
- run reale del 2026-04-04:
  - `run all` ha prodotto `raw` e `clean`, poi si e' fermato su `WinError 5` nel rename del run record
  - `run mart` eseguito separatamente con esito OK
  - output verificati:
    - clean `23.321` righe
    - mart `23.321` righe

## Analitico

- il v0 parte sul solo `2024`
- il perimetro corretto esclude `Codice Ente SSN = '000'`
- la domanda guida resta sulla prevenzione collettiva, ma il candidate lascia anche altre voci contabili per letture successive

## Cautele

- i dati sono contabili di spesa, non misurano esiti di salute
- gli enti `000` sono aggregazioni regionali e causano double-counting se sommati ai singoli enti
- alcuni codici voce sono aggregati di sezione e vanno trattati con prudenza nelle letture successive
- la serie storica 2012-2024 esiste, ma non entra nel primo ciclo tecnico
