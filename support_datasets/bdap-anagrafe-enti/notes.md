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

## Run

- **Run 2026-06-02**: RAW ✅ → CLEAN ✅ (38.196 righe, 63 colonne) → MART ✅ (1/1)
- **Tipo**: support dataset → non pubblicato su explorer, serve per join bridge
- **Join bridge**: espone 6 chiavi semantiche (istat_comune, istat_regione, provincia, codice_catastale, codice_ente, codice_scuola) → usata da `source-observatory/scripts/joinability_scan.py` per match indiretti

## Bridge columns (join keys)

| Chiave semantica | Colonna BDAP | Dataset collegati |
|---|---|---|
| `istat_comune` | `codice_istat_comune` | popolazione, ispra_ru, irpef, consumo_suolo, fsc, housing |
| `istat_regione` | `codice_regione` | aifa_spesa, bdap_lea, istat_gini, terna |
| `provincia` | `codice_provincia`, `sigla_provincia` | consip, openga, civile_flussi |
| `codice_catastale` | `codice_catastale` | irpef_comunale |
| `codice_ente` | `codice_ente_ipa`, `codice_ente_siope` | dipendenti_pubblici, bdap_entrate |
| `codice_scuola` | `codice_ente_miur` | mim_alunni, mim_anagrafica_scuole |

## Blocker

Nessuno noto.
