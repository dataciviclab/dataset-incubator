# Note

## Volume dati
2023: ~3.25M righe, 31 ZIP scaricati e mergiati. Il preprocess scarica incrementalmente (cache).

## Encoding
I CSV dentro gli ZIP sono latin-1. Il preprocess rileva e converte in utf-8.

## Nomi file
Alcuni nomi file contengono spazi (es. `EMILIA ROMAGNA`) e apostrofi (`VALLE D'AOSTA`). Il preprocess normalizza: spazi→trattini, apostrofi→underscore.

## Anni
2022 ha solo 12 file (dati comunali aggregati), 2023 ha 31 file (comuni per regione). Schema identico.
