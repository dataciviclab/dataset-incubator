# note - terna-electrical-energy-by-sector

## Shape

- **Fonte**: TERNA Download Center, dataset `ElectricalEnergy`
- **Formato**: XLSX, foglio `Export`
- **Colonne**: Anno, Regione, Provincia, Settore, Consumo (GWh)
- **Settori**: Domestico, Industria, Servizi, Agricoltura
- **Copertura**: 2015-2024, tutte le province italiane
- **Granularità**: annuale, per provincia e settore

## Note

- **Standardizzato nel clean**: il clean.sql aggrega con `SUM GROUP BY provincia, settore` — tutti gli anni hanno la stessa granularità (~428 righe/anno). 2015-2020 arrivano raw disaggregati (fino a 106k righe), ma il clean normalizza.
- **pageSize=500000** nell'API per non troncare anni con molti dati. Lo script `scripts/fetch_terna.py` rimuove la riga di footer "Applied filters" che DuckDB non gestisce.
- **Script source**: necessita `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` nell'ambiente.
- Si incrocia perfettamente con ElectricityBySource (produzione) per calcolare autoconsumo province
- Incrociabile con ISPRA emissioni GHG per impronta carbonica per settore
- Incrociabile con ISTAT popolazione per consumo pro-capite per provincia
