# note - terna-electrical-energy-by-sector

## Shape

- **Fonte**: TERNA Download Center, dataset `ElectricalEnergy`
- **Formato**: XLSX, foglio `Export`
- **Colonne**: Anno, Regione, Provincia, Settore, Consumo (GWh)
- **Settori**: Domestico, Industria, Servizi, Agricoltura
- **Copertura**: 2015-2024, tutte le province italiane
- **Granularità**: annuale, per provincia e settore

## Note

- **Schema drift**: 2015-2020 ~12.000 righe/anno (dati disaggregati per sotto-settore), 2021-2024 ~428 righe/anno (già aggregato per provincia). Il mart con SUM() normalizza, i totali sono comparabili.
- **pageSize=20000** necessario per coprire gli anni storici senza troncamento
- Si incrocia perfettamente con ElectricityBySource (produzione) per calcolare autoconsumo province
- Incrociabile con ISPRA emissioni GHG per impronta carbonica per settore
- Incrociabile con ISTAT popolazione per consumo pro-capite per provincia
