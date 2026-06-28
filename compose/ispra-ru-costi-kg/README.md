# ispra-ru-costi-kg

## Domanda

I territori che producono meno rifiuti urbani o raccolgono meglio spendono anche meno per abitante?

## Dataset

Nucleo multi-fonte ISPRA sui rifiuti urbani, costruito come estensione del vecchio `progetto-pilota`.

Fonti previste nel primo ciclo:

| ID | Fonte | Ruolo previsto | Stato |
|---|---|---|---|---|
| A | ISPRA RU base | base territoriale con totale RU, RD e popolazione | run verde `2010-2024` (espanso da 5 a 15 anni) |
| B | ISPRA kg per abitante | metrica pro capite del volume di RU | run verde `2020-2024`, mart cross mancante nel `2022` sul clone corrente |
| C | ISPRA costo per abitante | asse economico minimo del servizio | run verde `2020-2024`, mart cross mancante nel `2021` sul clone corrente |

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

## Output disponibili oggi

Il filone ha già superato il primo gate tecnico.

Output già disponibili:

- `sources/a_ru_base` con `mart_comuni`
- `sources/b_kg_per_abitante` con `mart_comuni`
- `sources/c_costo_per_abitante` con `mart_comuni`
- `compose/sql/mart_cross_comuni.sql` come layer cross del filone
- `compose/sql/mart_compose_v2.sql` come primo layer `v2` costo-performance
- notebook `v0`
- notebook `v1` con prima lettura pubblica già riusata nella Discussion `#22`

Sul clone corrente, il cross mart è fisicamente disponibile per:

- `2020`
- `2023`
- `2024`

Gli anni `2021` e `2022` non sono oggi presenti nel cross mart locale per un vincolo operativo di sync/lock OneDrive sui run delle sorgenti `C` e `B`.

Stato attuale del candidate:

- source dataset `A` eseguito su `2010-2024` (15 anni), `B/C` su `2020-2024`
- compose minimo chiuso sul join `codice_comune_istat x anno`
- notebook `v1` disponibile sul perimetro joinato
- per vincolo del toolkit, il SQL del cross resta anche in `sources/a_ru_base/sql/` come copia eseguibile

## Criterio di promozione

Promuovere il filone solo se:

- il join tra A/B/C è stabile sul perimetro comune
- gli anni comuni bastano per una prima lettura difendibile
- `costo per abitante` e `kg per abitante` sono abbastanza comparabili da non trasformare il notebook in un solo caveat metodologico
- emerge una domanda pubblica chiara su costo, volume e performance del servizio

## Stato

- candidate attivo con `v1` disponibile

## Domande complementari

- i territori con meno `kg per abitante` spendono anche meno?
- i territori con più raccolta differenziata hanno costi pro capite più bassi, più alti o semplicemente diversi?
- il costo per abitante segue il volume dei RU o emergono profili territoriali più complessi?

## Provenienza

Il filone nasce come estensione ordinata del vecchio `progetto-pilota` ISPRA RU, oggi classificato come `legacy closed` in `dataciviclab`.

## Gap noti / follow-up

- **B** e **C**: lo schema dei CSV dei costi è cambiato tra 2011 e 2020 (11 colonne costo nel 2011 → 6 nel 2020). Impossibile espandere linearmente come A. Serve analisi separata con SQL condizionale per anno o skip colonne adattivo.

## Prossimo passo

Il prossimo step non è più costruire il `v1`, ma definire e chiudere il `v2`.

Perimetro operativo del `v2`:

- base principale: `2024`
- contesto evolutivo: `2020`, `2023`, `2024`
- ponte metodologico con il `progetto-pilota`: confronto `2020 -> 2023`

Direzioni già approvate in `#33`:

- riusare la logica dei quadranti del `progetto-pilota`
- aggiungere un nuovo `quadrante_costo` su livello `2024`
- usare come soglie le mediane del campione joinato `A + B + C` nel `2024`
- tenere il join ISTAT popolazione come robustezza successiva, non come blocco iniziale
- chiudere il mart `v2` anche senza join ISTAT, con nota metodologica dedicata ai comuni turistici
