# istat_elenco_comuni

**Fonte**: ISTAT SITUAS — Sistema Informativo Territoriale delle Unità Amministrative e Statistiche
**Endpoint**: `https://situas-servizi.istat.it/publish/reportspooljson?pfun=...`

## Contenuto

Elenco completo dei comuni italiani (7.894) con:
- Codice ISTAT (PRO_COM_T, 6 caratteri)
- Denominazione ufficiale
- Codice catastale (Belfiore)
- Superficie in km²
- Popolazione residente e legale
- Regione, provincia, sigla automobilistica
- Zona altimetrica, altitudine, litoraneità/insularità

## Come rigenerare i dati

Prerequisito: `pip install opensituas`

```bash
python scripts/download_data.py
```

Questo script chiama `opensituas get 61/73/74` e produce il CSV unificato in `raw/`.

## Run

```bash
python -m toolkit.cli.app run all --config dataset.yml --year 2026
```

## Note

- Fonte: ISTAT SITUAS via opensituas (https://github.com/ondata/opensituas)
- Snapshot alla data 09/06/2026
- La superficie è in km² con separatore decimale standard (punto)
- Codice catastale = codice Belfiore (4-5 caratteri, es. "A074" per Agliè)
