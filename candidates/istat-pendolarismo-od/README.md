# Pendolarismo — matrice origine-destinazione per comune (2021)

## Domanda

- Quanto è autosufficiente il mercato del lavoro di ogni comune? Quanti residenti escono,
  quanti entrano, e verso dove?
- Quali comuni sono dormitori (quasi tutti escono) e quali poli di attrazione (quasi tutti
  entrano)?
- Quanto pesa il pendolarismo scolastico rispetto a quello per lavoro?

## Dataset

- fonte: ISTAT, Censimento permanente 2021 — matrici origine-destinazione degli spostamenti
  giornalieri, due file: **lavoro** (`matrix_pendoLAVORO_2021.zip`) e **studio**
  (`matrix_pendoSTUDIO_2021.zip`)
- formato: ZIP → TXT tab-delimited, CRLF, header, codici ISTAT a 6 cifre
- licenza: CC BY (ISTAT), nessuna autenticazione
- copertura: **una sola edizione** (2021, pubblicata il **2/10/2025**, nota metodologica
  aggiornata il 3/11/2025). Non esistono file 2022-2024: gli URL rispondono HTTP 200 ma con
  una pagina HTML di errore da ~5 KB, non uno ZIP
- **è una stima modellata, non un conteggio**: ISTAT integra il censimento 2021 (campione)
  con Registro Base degli Individui, dati INPS e Certificazione Unica/Anagrafe Tributaria e
  una matrice di distanze intercomunali. Pendolare = occupato che si reca almeno 3 giorni a
  settimana al lavoro, partendo dall'alloggio e rientrando ogni giorno; esclusi chi lavora
  da casa o non ha sede fissa. I flussi sotto soglia di riservatezza non sono pubblicati
- volumi: **523.949 coppie** lavoro + **141.226** studio = **665.175 righe**;
  19.565.808 spostamenti per lavoro (9.803.786 intra-comune + 9.762.022 inter) e
  9.279.329 per studio

## Perché vale la pena testarlo

- è il tassello **territorio / accesso alle opportunità**: trasforma "dove sono le case" in
  "dove sono le case rispetto al lavoro"
- si combina con `istat_abitazioni_censimento`: un comune con il 60% di case vuote e forte
  deflusso pendolare racconta una storia diversa da uno autosufficiente
- copertura completa (7.904 comuni di origine), codici puliti, due download

## Output minimo atteso

- `clean`: 665.175 righe, motivo (`lavoro`/`studio`), comune di residenza, comune di
  destinazione, pendolari
- `mart_comuni_pendolarismo`: 7.904 comuni con intra, uscenti, entranti, saldo e
  auto-contenimento (lavoro) + uscenti/entranti studio
- `mart_flussi_top`: le 200 coppie inter-comune più consistenti **complessivamente** (nel
  2021: 190 lavoro + 10 studio), con entrambi i nomi. Chi filtra `motivo = 'studio'` trova
  10 righe, non 200: per i volumi per motivo usare `mart_comuni_pendolarismo`

## Verifica (numeri chiave)

| Controllo | Valore |
|---|---|
| Lavoro: intra + inter | 9.803.786 + 9.762.022 = **19.565.808** ✓ |
| Studio: intra + inter | 6.632.917 + 2.646.412 = **9.279.329** ✓ |
| Comuni di origine / destinazione (lavoro) | 7.904 / 7.903 |
| Primo flusso inter-comune | Guidonia Montecelio → Roma **17.299** |
| Polo con il saldo maggiore | Milano **+286.727** (384.744 entranti, 98.017 uscenti) |
| Comune con auto-contenimento minimo (pop>5.000) | Verderio (LC) **7,9%** |

## Il nodo dei codici sardi (risolto)

Il primo run aveva **394 comuni senza nome**, 377 sardi. La causa non era un crosswalk
mancante ma **l'anagrafica sbagliata**: `istat_elenco_comuni` (2026) usa i nuovi codici
provinciali sardi **112-119** della riforma 2025, mentre la matrice 2021 usa la generazione
precedente (090/091/092/095/111). `comuni_master` conserva quella generazione e copre
**7.887 comuni su 7.904 (99,8%)**.

Restano **17 comuni** senza nome (fusioni recenti, 7 province: 005, 012, 013, 018,
024, 025, 028), per
**9.917 uscenti — lo 0,1%**. Il mart li tiene con nome `NULL` e `in_anagrafica = false`
invece di scartarli, e nei 200 flussi top non manca nessun nome (il 6° flusso nazionale è
Quartu Sant'Elena → Cagliari, 9.501).

## Criterio di promozione

- run verde con `toolkit` (2/2 mart, quality score 100)
- readiness 8/8
- 17 comuni residui da mappare per la copertura completa (non bloccante)

## Stato

- candidate implementato e verificato in locale (2026-11-23)
- issue di intake: #951

## Prossimo passo

- mappare i 17 comuni residui (fusioni) se serve copertura completa
- analysis: "Chi esce, chi entra, e dove" — mappa dei dormitori e dei poli
- il 2011 è disponibile (`DF_BULK_CPO2011_DICA_PEND`) ma con codici e perimetro diversi:
  eventuale confronto, non serie
