# BDAP Anagrafe Enti — Support Dataset

## Tipo

**Support dataset** — serve per arricchimento e join con altri dataset (es. copertura open data dei portali PA).

## Fonte

MEF — Ragioneria Generale dello Stato / OpenBDAP
URL: https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/745861d3-e741-43ff-b68a-7cf357aab888.csv
Aggiornato al 23/04/2026. Licenza: Creative Commons Attribution.

## Schema

63 colonne — anagrafe completa degli enti pubblici italiani (Id_Ente, Denominazione, CF/PIVA, indirizzo, codici IPA/SIOPE/ISTAT, etc.).

## Uso previsto

Join con altri dataset per arricchire enti con denominazione, territorio, codici IPA.

## Run

```bash
cd toolkit
python -m toolkit.cli.app run all --config ../dataset-incubator/support_datasets/bdap-anagrafe-enti/dataset.yml
```
