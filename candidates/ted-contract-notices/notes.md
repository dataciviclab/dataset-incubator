# Note tecniche — TED Contract Notices

## Fonte

- **URL ZIP**: `https://data.europa.eu/api/hub/store/data/ted-contract-notices-{YEAR}.zip`
- **CSV interno**: `export_CFC_{YYYY}.csv` (1 file per ZIP)
- **Formato**: UTF-8, delimitatore virgola, quoted fields
- **Anni**: 2020–2023 verificati funzionanti (2012–2019 disponibili su richiesta)
- **Licenza**: EU Open Data — riutilizzo libero

## Pipeline

- `extractor: unzip_first_csv` — estrae automaticamente il primo CSV dallo ZIP
- `clean.read`: delim=",", encoding="utf-8", quote='"'

## Schema clean

64 colonne in ingresso, filtrate per ISO_COUNTRY_CODE='IT'. Tutti i campi rilevanti sono rinominati in italiano.

### Colonne notevoli

- `VALUE_EURO`: valore stimato. Alcuni valori usano virgola come separatore decimale — `REPLACE(..., ',', '.')` nel clean.
- `DT_DISPATCH`, `DT_APPLICATIONS`: formato `DD/MM/YY` — parsing con `STRPTIME`.
- `ADDITIONAL_CPVS`: codici CPV aggiuntivi separati da `---`.
- `ID_LOT`: numero del lotto quando il bando è suddiviso in lotti. Ogni lotto è una riga separata.
- `CPV`: codice CPV principale a 8 cifre (es. `72200000`).
- `TAL_LOCATION_NUTS`: codice NUTS del luogo di esecuzione (es. `ITH31` per Verona).

### Filtro Italia

Il filtro `ISO_COUNTRY_CODE = 'IT'` cattura i bandi pubblicati da stazioni appaltanti italiane. Alcuni bandi con stazione estera ma esecuzione in Italia potrebbero uscire con paese diverso — per quelli serve `TAL_LOCATION_NUTS LIKE 'IT%'`. Al momento il filtro è sul paese della stazione appaltante.

## Relazioni con altri dataset

- **ANAC bandi_gara**: i CPV TED sono allineati con la codifica europea usata da ANAC. SI può joinare su `cpv_codice` (prime 8 cifre).
- **comuni_master**: join su NUTS per arricchimento territoriale.
- **RNA**: join su `stazione_appaltante_codice_nazionale` (codice fiscale/partita IVA).

## Limiti noti

- TED pubblica solo bandi **sopra soglia UE** (salvo pubblicazioni volontarie). I bandi sotto soglia sono su ANAC.
- Il dato arriva **aggiornato al 2023** — verificare se 2024+ è disponibile con pattern URL diverso.
- `ADDITIONAL_CPVS` è una stringa con separatore `---`, non normalizzata. Un parsing più fine può essere fatto nel mart.
- I valori monetari possono avere formati diversi (punto vs virgola) in alcuni anni — monitorare con `schema_diff`.

## Rischio schema drift

Il formato TED CSV è stabile (stesse 64 colonne identificate in anni diversi), ma cambi di schema XSD potrebbero introdurre variazioni. Usare `toolkit schema_diff` per monitorare.
