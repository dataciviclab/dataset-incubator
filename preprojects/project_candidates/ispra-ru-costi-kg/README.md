# ispra-ru-costi-kg

## Domanda

I territori che producono meno rifiuti urbani o raccolgono meglio spendono anche meno per abitante?

## Dataset

Nucleo multi-fonte ISPRA sui rifiuti urbani, costruito come estensione del vecchio `progetto-pilota`.

Fonti previste nel primo ciclo:

| ID | Fonte | Ruolo previsto | Stato |
|---|---|---|---|
| A | ISPRA RU base | base territoriale con totale RU, RD e popolazione | da riallineare al pilota legacy |
| B | ISPRA kg per abitante | metrica pro capite del volume di RU | da verificare |
| C | ISPRA costo per abitante | asse economico minimo del servizio | da verificare |

## Perche vale la pena testarlo

- rafforza il bucket ambiente con un filone civicamente leggibile
- evita il solo ranking sui rifiuti e introduce un asse costo/performance
- riusa il lavoro gia emerso nel `progetto-pilota`, ma lo riporta dentro il flusso del Lab
- puo produrre un mart semplice e riusabile anche per follow-up successivi

## Architettura adottata

Pattern multi-fonte, stile `malasanita`:

- una cartella `sources/` per ogni tabella sorgente
- un `compose/` finale che legge solo output gia puliti o aggregati
- promozione possibile solo dopo verifica reale di:
  - chiavi di join
  - overlap temporale
  - comparabilita minima delle metriche

## Output minimo atteso

- nota breve su compatibilita di anni, granularita e chiavi territoriali
- primo join di prova tra le tre tabelle
- mart minimo `territorio x anno` con:
  - `kg_per_abitante`
  - `costo_per_abitante`
  - `% raccolta differenziata`, se gia disponibile e compatibile
- decisione finale:
  - filone promettente
  - support dataset
  - stop

## Criterio di promozione

Promuovere il filone solo se:

- il join tra A/B/C e stabile sul perimetro comune
- gli anni comuni bastano per una prima lettura difendibile
- `costo per abitante` e `kg per abitante` sono abbastanza comparabili da non trasformare il notebook in un solo caveat metodologico
- emerge una domanda pubblica chiara su costo, volume e performance del servizio

## Stato

- intake

## Domande complementari

- i territori con meno `kg per abitante` spendono anche meno?
- i territori con piu raccolta differenziata hanno costi pro capite piu bassi, piu alti o semplicemente diversi?
- il costo per abitante segue il volume dei RU o emergono profili territoriali piu complessi?

## Provenienza

Il filone nasce come estensione ordinata del vecchio `progetto-pilota` ISPRA RU, oggi classificato come `legacy closed` in `dataciviclab`.

## Prossimo passo

- documentare le tre fonti in `sources/`
- verificare URL, formato, chiavi e annualita comuni
- decidere il primo perimetro reale del `compose/`
