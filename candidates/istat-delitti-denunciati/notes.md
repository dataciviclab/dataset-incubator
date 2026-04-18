# Note sul Dataset ISTAT - Delitti Denunciati

## Descrizione del Flusso
Il dataset viene estratto dal mirror pubblico **DBnomics** del provider ISTAT. La fonte primaria desiderata resta l'endpoint SDMX ISTAT `73_67`, ma la chiamata diretta e' risultata instabile in fase di run locale anche su query ristrette. DBnomics espone lo stesso provider/dataset in CSV e permette di produrre output riproducibili.

Questa scelta va trattata come compromesso operativo, non come sostituzione definitiva della fonte primaria.

## Logica di Trasformazione (ETL)
- **Layer Raw**: Scarica il CSV DBnomics `ISTAT/73_67_DF_DCCV_DELITTIPS_1`.
- **Layer Clean**: Converte il CSV wide in formato long e filtra gli anni 2010-2015.
- **Layer Mart**: Fornisce una vista tabellare pulita e tipizzata, pronta per l'analisi statistica o la visualizzazione.

## Dettagli sui Dati
- **Copertura Temporale**: Serie storica dal 2010 al 2015.
- **Partizione runtime**: `dataset.yml` usa il solo anno runtime 2015 per produrre una singola partizione che contiene la serie storica 2010-2015.
- **Metriche**: Il valore rappresenta il numero di delitti denunciati per specifica categoria e area geografica.
- **Mapping Reati**: I codici (es. `INTENHOM`, `THEFT`, `RAPE`) corrispondono alla classificazione ufficiale ISTAT/Ministeriale dei delitti. Nel mart iniziale la label `reato` coincide con il codice per evitare mapping manuali non verificati.

## Avvertenze
- Dipendenza da mirror: il raw dipende da DBnomics, che replica dati ISTAT ma non e' la fonte primaria.
- Fonte primaria: in caso di passaggio futuro alla fonte SDMX diretta, verificare la disponibilita' dell'endpoint e riallineare i nomi dimensione usati dal plugin.
- Perimetro geografico: il candidate iniziale copre il totale Italia (`REF_AREA=IT`), non regioni/province.
- Notebook: l'analisi deve leggere il mart generato e non introdurre mapping o claim non verificati.
