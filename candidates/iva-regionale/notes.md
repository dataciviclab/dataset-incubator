# Notes — iva-regionale

## Stato

Candidate a standard v1 (2026-08-01): schema esteso con le frequenze MEF,
mart analitiche serie (regioni_anno / sintesi_nazionale / trend_regioni).

## Copertura

| Anno d'imposta | URL presentazione | Righe |
|:--------------:|:-----------------:|:-----:|
| 2014 | 2015 | 21 |
| 2015 | 2016 | 21 |
| … | … | … |
| 2023 | 2024 | 21 |

## Anni disponibili (per espansione)

Tutti gli anni dal 2009 al 2024 funzionano (16 anni totali). Attivi 2014-2023.

## Note tecniche

- Fonte scaricata via `http_file` (URL MEF con `{year}` nel path); header
  sempre alla riga 9 (verificato 5/5 anni: 2015, 2018, 2020, 2022, 2024) —
  `read.skip: 9` + `null_padding: true` (riga finale con 1 solo campo)
- Numeri raw in formato italiano (punti migliaia, virgola decimale):
  letti come VARCHAR, normalizzati con le macro standard
  (`normalize_italian_integer` / `normalize_italian_number`)
- I valori raw sono in migliaia di euro; il clean moltiplica ×1000 per avere euro
- `***` = data masking (meno di 3 contribuenti) → NULL
- Niente più preprocess.py: migrato a http_file (2026-08-01)
- clean.sql usa le **macro standard** del toolkit (cast_bigint, cast_double,
  normalize_string, normalize_italian_*)

## Decisioni metodologiche (2026-08-01)

### "Non indicata" esclusa dal clean
Il raw MEF ha 23 righe: 21 regioni + `TOTALE` + `Non indicata`. Il clean
esclude le ultime due (`NOT IN ('TOTALE', 'Non indicata')`). Motivo:
- `TOTALE` è un doppione dell'aggregazione, ricalcolata nelle mart
- `Non indicata` non è una regione: nel ranking/quota distorcerebbe l'analisi
- Costo: i totali nazionali delle mart sono "somma delle 21 regioni
  dichiarate" (~4.649 mld 2023), non il totale MEF (~4.737 mld). Delta ~1,9%.
  Documentato nel README. Se un'analisi richiede il totale ufficiale MEF,
  va aggiunta la riga TOTALE esplicitamente — NON abilitare "Non indicata".

### Frequenze nel clean
Prima il clean esponeva solo gli Ammontare (9 colonne): le Frequenze MEF
(quante partite IVA dichiarano ogni voce) erano scartate. Questo rendeva
inutilizzabili i calcoli pro-capite e l'analisi credito vs debito. Ora il
clean espone le 5 frequenze (14 colonne). Le medie MEF non servono: si
ricalcolano come Ammontare/Frequenza.

### Denominatori pro-capite
`va_per_dichiarante` usa `va_frequenza` come denominatore, non
`contribuenti`. Verifica Lombardia 2023: 472.7k€ (frequenza) vs 458.7k€
(contribuenti totali — distorto, include chi non dichiara VA).

## Viste disponibili (per v1)

- 0201: Regione (fatta)
- 0202: Settore ATECO (lettera)
- 0203: Classe volume d'affari
- 0204: Tipo soggetto
