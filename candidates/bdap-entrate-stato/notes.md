# Notes

## Tecnico

- fonte ufficiale verificata nella discussion `#154` e nel source-check del `2026-03-31`
- URL usato nel candidate:
  `https://bdap-opendata.rgs.mef.gov.it/export/csv/Rendiconto-Pubblicato---Serie-storica---Entrate-Aggregato-per-Titolo-Natura-Tipologia-e-Provento.csv`
- il file e un export storico cumulativo: il run year usato nel candidate e `2024`, ma il contenuto copre `2008-2024`
- delimitatore reale verificato: `;`
- encoding reale da trattare in lettura: `cp1252` / `latin-1`
- il CSV termina con un separatore finale: la lettura config assegna una colonna tecnica extra (`column11`) poi ignorata nel `clean`
- cardinalita osservata sul dump verificato il `2026-04-13`: `1321` righe totali inclusa header

## Analitico

- il v0 resta nel perimetro `Datasets`: niente claim su tenuta effettiva del gettito
- lettura minima consigliata: composizione per `Titolo` e distinzione `ricorrenti / non ricorrenti`
- anni guida per il notebook v0: `2008`, `2020`, `2024`

## Cautele

- `Previsioni Definitive CP/CS` non equivalgono a incasso effettivo
- la domanda pubblica va formulata come lettura del perimetro autorizzato a consuntivo, non come misura diretta della riscossione
- eventuali confronti lunghi richiedono prudenza sulla stabilita delle classificazioni contabili
- il dataset riguarda lo Stato centrale, non il perimetro consolidato delle amministrazioni pubbliche

## Stato operativo

- scaffold iniziale creato su branch `intake/bdap-entrate-stato`
- issue intake aperta: `https://github.com/dataciviclab/dataset-incubator/issues/133`
- `validate_candidate_structure.py` eseguito con esito OK
- `toolkit inspect paths` OK: `effective_root` risolve a `dataset-incubator/out`
- run reale eseguito il `2026-04-13`
  - comando (venv toolkit): `/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python -m toolkit.cli.app run all --config ../dataset-incubator/candidates/bdap-entrate-stato/dataset.yml`
  - run_id: `20260413T122412Z_fb39bdf2`
  - esito: `SUCCESS`
  - output verificati:
    - clean `1320` righe
    - mart `104` righe
- warning mart presente ma non bloccante: rimozione attesa di colonne di dettaglio nel passaggio `clean -> mart`
- verdict intake: `runnable`

### Nota ambiente (venv)

- se il terminale e aperto in `dataset-incubator`, usare comunque la venv del repo `toolkit` per i comandi CLI:
  - `/home/gabry/dev/dataciviclab-workspace/toolkit/.venv/bin/python -m toolkit.cli.app ...`
- il comando `toolkit ...` puo fallire con `exit 127` quando la shell non ha la venv toolkit attiva