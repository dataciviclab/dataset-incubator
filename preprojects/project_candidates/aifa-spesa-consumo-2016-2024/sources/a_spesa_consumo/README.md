# Source A - spesa e consumo AIFA 2016-2024

Fonte principale del candidate. Contiene entrambi i flussi (`convenzionata` e `tracciabilita`)
nello stesso file, con null strutturali per il flusso non applicabile a ciascuna riga.

## Perimetro attivo

Solo flusso `convenzionata`. Il clean filtra le righe con `spesa_convenzionata IS NOT NULL`.

## Campi usati

- `anno`, `mese`: copertura temporale
- `codreg`, `regione`: territorio (21 regioni/PA)
- `classe`, `atc1..4` + descrizioni: gerarchia terapeutica
- `numero_confezioni_convenzionata`: volumi dispensati
- `spesa_convenzionata`: spesa SSN lorda

## Procedura download

I file non hanno URL parametrico. Scaricare manualmente dalla pagina AIFA e rinominare:

```
aifa_spesa_consumo_2016.csv
aifa_spesa_consumo_2017.csv
...
aifa_spesa_consumo_2024.csv
```

Posizionare in: `out/data/raw/aifa_spesa_consumo/{year}/aifa_spesa_consumo_{year}.csv`

URL per anno documentati in `../../notes.md`.

## Da verificare

- nomi colonna esatti (vedere `../../notes.md` sezione Tecnico - GATE manuale)
- encoding effettivo (atteso UTF-8-BOM, verificare su primo run)
- presenza o assenza di riga header nel file reale
