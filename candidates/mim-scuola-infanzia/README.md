# mim-scuola-infanzia

**Domanda guida:** Quanti bambini italiani e non italiani frequentano le scuole dell'infanzia statali? Come si distribuisce la presenza straniera per territorio?

**Fonte:** Ministero dell'Istruzione e del Merito — dati.istruzione.it
**Dataset:** INFANZIASTRACITSTA
**Formato:** CSV, 4 colonne, ~300 KB/anno
**Granularità:** scuola (riconducibile a comune via anagrafica MIM)
**Copertura:** 2018–2025 (8 anni scolastici)
**Licenza:** CC BY (MIM Open Data)

## Schema output (14 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno_scolastico` | VARCHAR | Anno scolastico (es. 202425) |
| `codice_scuola` | VARCHAR | Codice unico scuola |
| `denominazione_scuola` | VARCHAR | Nome della scuola |
| `grado_istruzione_scuola` | VARCHAR | Grado (es. SCUOLA INFANZIA) |
| `caratteristica_scuola` | VARCHAR | Normale / speciale |
| `bambini_italiani` | INTEGER | Bambini con cittadinanza italiana |
| `bambini_non_italiani` | INTEGER | Bambini con cittadinanza non italiana |
| `bambini_totale` | INTEGER | Somma italiani + non italiani |
| `area_geografica` | VARCHAR | Nord Ovest, Nord Est, Centro, Sud, Isole |
| `regione` | VARCHAR | Regione |
| `provincia` | VARCHAR | Provincia |
| `comune` | VARCHAR | Comune |
| `codice_comune_scuola` | VARCHAR | Codice catastale comune |
| `denominazione_istituto_riferimento` | VARCHAR | Istituto di riferimento |

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/mim-scuola-infanzia/dataset.yml
```

## Issue di riferimento

- Intake: [#553](https://github.com/dataciviclab/dataset-incubator/issues/553)
