# Notes — bdap-anagrafe-enti

## Support dataset

Dataset di anagrafe enti pubblici italiani. Fonte primaria per join su codici ente (IPA, SIOPE, ISTAT, SSN).

## Fonte

- URL: `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/745861d3-e741-43ff-b68a-7cf357aab888.csv`
- Formato: CSV, `;` delim, `cp1252` encoding
- Colonne: 63
- Righe: ~38k enti

## Schema

- Chiave primaria: `id_ente`
- Codici join: `codice_ente_ipa`, `codice_ente_siope`, `codice_regione`, `codice_provincia`
- Dati anagrafici: `denominazione`, `cf`, `piva`, `indirizzo`, `cap`, `telefono`, `url`
- Territorio: `codice_istat_comune`, `dizione_comune`, `codice_regione`, `dizione_regione`

## Note tecniche

- Encoding `cp1252` (Windows Latin-1)
- Delimitatore `;`
- Header row presente
- 63 colonne — molte sono codici e descrizioni per diversi registri (IPA, SIOPE, ISTAT, MIUR, etc.)

## Blocker

Nessuno noto.
