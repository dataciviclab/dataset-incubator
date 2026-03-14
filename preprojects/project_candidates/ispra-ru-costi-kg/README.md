# ispra-ru-costi-kg

## Domanda

I territori che producono meno rifiuti urbani o raccolgono meglio spendono anche meno per abitante?

## Dataset

Nucleo multi-fonte ISPRA sui rifiuti urbani, costruito come estensione del vecchio `progetto-pilota`.

Fonti previste nel primo ciclo:

| ID | Fonte | Ruolo previsto | Stato |
|---|---|---|---|
| A | ISPRA RU base | base territoriale con totale RU, RD e popolazione | run verde `2020-2024` |
| B | ISPRA kg per abitante | metrica pro capite del volume di RU | run verde `2020-2024` |
| C | ISPRA costo per abitante | asse economico minimo del servizio | run verde `2020-2024` |

## Perché vale la pena testarlo

- rafforza il bucket ambiente con un filone civicamente leggibile
- evita il solo ranking sui rifiuti e introduce un asse costo/performance
- riusa il lavoro già emerso nel `progetto-pilota`, ma lo riporta dentro il flusso del Lab
- può produrre un mart semplice e riusabile anche per follow-up successivi

## Architettura adottata

Pattern multi-fonte, stile `malasanita`:

- una cartella `sources/` per ogni tabella sorgente
- un `compose/` finale che legge solo output già puliti o aggregati
- promozione possibile solo dopo verifica reale di:
  - chiavi di join
  - overlap temporale
  - comparabilità minima delle metriche

## Output minimo atteso

- nota breve su compatibilità di anni, granularità e chiavi territoriali
- primo join di prova tra le tre tabelle
- mart minimo `territorio x anno` con:
  - `kg_per_abitante`
  - `costo_per_abitante`
  - `% raccolta differenziata`, se già disponibile e compatibile
- decisione finale:
  - filone promettente
  - support dataset
  - stop

Output ora disponibili nel primo step:

- `sources/a_ru_base` con `mart_comuni`
- `sources/b_kg_per_abitante` con `mart_comuni`
- `sources/c_costo_per_abitante` con `mart_comuni`
- `sources/a_ru_base/sql/mart_cross_comuni.sql` come primo compose comunale minimo
- notebook `v0` sul perimetro joinato `A + B + C`

Stato attuale del candidate:

- source dataset `A/B/C` eseguiti su `2020-2024`
- compose minimo chiuso sul join `codice_comune_istat x anno`
- notebook `v0` disponibile sul perimetro joinato

## Criterio di promozione

Promuovere il filone solo se:

- il join tra A/B/C è stabile sul perimetro comune
- gli anni comuni bastano per una prima lettura difendibile
- `costo per abitante` e `kg per abitante` sono abbastanza comparabili da non trasformare il notebook in un solo caveat metodologico
- emerge una domanda pubblica chiara su costo, volume e performance del servizio

## Stato

- intake

## Domande complementari

- i territori con meno `kg per abitante` spendono anche meno?
- i territori con più raccolta differenziata hanno costi pro capite più bassi, più alti o semplicemente diversi?
- il costo per abitante segue il volume dei RU o emergono profili territoriali più complessi?

## Provenienza

Il filone nasce come estensione ordinata del vecchio `progetto-pilota` ISPRA RU, oggi classificato come `legacy closed` in `dataciviclab`.

## Prossimo passo

- decidere se il filone resta ancora un candidate tecnico o è pronto per una prima discussione pubblica
- capire se il prossimo output debba restare sul `2024` o allargarsi a una lettura `2020-2024`
- chiarire quali profili territoriali meritano un notebook `v1` più forte
