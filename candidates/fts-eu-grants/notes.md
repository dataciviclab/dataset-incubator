# Note tecniche — FTS EU Grants

## Fonte

- **URL XLSX**: `https://ec.europa.eu/budget/financial-transparency-system/download/{YEAR}_FTS_dataset_en.xlsx`
- **Formato**: XLSX, 38 colonne, primo sheet
- **Anni**: 2020–2024 verificati funzionanti (2007–2019 disponibili su richiesta)
- **HEAD richiesto**: il server Europa restituisce `Content-Length: 0` su HEAD ma il file è correttamente servito su GET (chunked encoding)
- **Licenza**: EU Open Data

## Pipeline

- `type: script` esegue `scripts/convert_xlsx_to_csv.py` che scarica l'XLSX e produce un CSV normalizzato
- Lo script usa `pandas.read_excel(dtype=str)` per leggere tutto come stringhe, evitando problemi di tipo tra anni
- `clean.read` legge il CSV prodotto dallo script (non l'XLSX diretto)
- Richiede `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` per abilitare lo script source

## Schema clean

38 colonne normalizzate in italiano. Le colonne importi usano la virgola come separatore delle migliaia in alcune celle — `REPLACE(..., ',', '')` nel clean rimuove le virgole prima del cast a DOUBLE.

### Filtro Italia

Il filtro `paese_beneficiario = 'Italy'` usa il nome completo del paese (non ISO). Copre i beneficiari con sede legale in Italia — non necessariamente i progetti che si svolgono in Italia.

### Differenza con OpenCoesione / RNA

- **FTS** copre solo la gestione diretta UE (Commissione europea)
- **OpenCoesione** copre i fondi strutturali (gestione condivisa con Stati membri)
- **RNA** copre gli aiuti di Stato (erogati da enti italiani, non UE)

Insieme danno una visione quasi completa dei flussi finanziari pubblici verso l'Italia.

## Colonne notevoli

- `beneficiario_nome`: può contenere `*****` per motivi di privacy (persone fisiche)
- `importo_contrattato`: l'importo effettivamente contrattualizzato
- `importo_consumato_stimato`: quanto è stato effettivamente speso (stimato)
- `nome_programma`: include il programma UE (es. "1.0.23 - Digital Europe Programme")

## Limiti noti

- I dati FTS coprono solo la gestione diretta UE (~20% del budget UE). I fondi strutturali (80%) sono altrove (OpenCoesione, ESIF, Kohesio).
- Alcuni beneficiari sono offuscati (`*****`) per motivi di privacy.
- I nomi dei programmi non sono normalizzati — il raggruppamento per categoria è fatto nel mart.
- Le date progetto possono essere vuote.

## Rischio schema drift

Il formato XLSX è stabile dal 2007. Le colonne non cambiano, ma nuovi programmi possono aggiungere nuovi codici.
