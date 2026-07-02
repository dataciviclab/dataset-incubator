# silos-infrastrutture

**SILOS** — Sistema Informativo Legislativo Opere Strategiche (Camera dei Deputati).

Report annuale del Servizio Studi che censisce lo stato di attuazione delle infrastrutture strategiche e prioritarie in Italia.

- **Fonte**: https://dati.camera.it/ocd/dump/silos/PISRapportoCSV2024.zip
- **Licenza**: CC BY-SA 4.0
- **Copertura**: 2024 (report annuale, serie storica dal 2004)
- **Granularità**: singolo intervento con CUP, localizzazione, soggetto competente, stato attuazione

## Domanda civica

Dove sono finite le infrastrutture strategiche? Quali opere sono in ritardo e in quali regioni?

## Shape

- 3.527 righe, 15 colonne
- 13 sistemi infrastrutturali (Ferrovie, Strade e autostrade, Sistemi urbani, Porti e interporti, Aeroporti, Ponte sullo Stretto, Mo.S.E., Infrastrutture Idriche, Ciclovie, Edilizia pubblica, Energia, Telecomunicazioni, Altre infrastrutture)
- Costi, disponibilità e fabbisogno in milioni di euro
- Joinabile con `mit_opere_incompiute_2020` (stesso dominio: CUP, localizzazione)

## Perché vale la pena

- Unico dataset strutturato sulle opere strategiche in Italia
- 20 anni di serie storica (report annuali dal 2004)
- Colonna CUP per join incrociati

## Output minimo atteso

- Dataset pulito e interrogabile via SQL
- Risposta alla Discussion #286 con dati verificati
