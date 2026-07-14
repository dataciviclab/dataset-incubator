# MUR Iscritti — Note Implementative

## Approccio

Stessa strategia di `mur_immatricolati`: `http_file` con URL CSV diretto invece del plugin CKAN.

## Risorsa scelta

`Iscritti per ateneo` — la più semplice e stabile:
- 25 anni accademici (2000/01 – 2024/25)
- 4.356 righe
- Colonne: AnnoA, AteneoNOME, AteneoCOD, SESSO, Isc

## Encoding

Il CSV è in latin-1. Specificato `encoding: "latin-1"` in dataset.yml.

## Altre risorse disponibili

Il CKAN espone 24 risorse per `iscritti`. Tra le più interessanti:
- `Iscritti per classe` — per classe di laurea (sconsigliato: API DataStore 404)
- `Iscritti per ateneo e gruppo` — per gruppo disciplinare
- `Iscritti per corso di studi` — per corso, anni più limitati (2010-2025)

Per v0 si tiene solo `Iscritti per ateneo`. Future espansioni possono aggiungere altre risorse.
