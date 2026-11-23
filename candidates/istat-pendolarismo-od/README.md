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
- copertura: **una sola edizione** (2021, pubblicata 2/10/2025). Non esistono file 2022-2024:
  gli URL rispondono HTTP 200 ma con una pagina HTML di errore da ~5 KB, non uno ZIP
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
- `mart_flussi_top`: le 200 coppie inter-comune più consistenti, con entrambi i nomi

## Verifica (numeri chiave)

| Controllo | Valore |
|---|---|
| Lavoro: intra + inter | 9.803.786 + 9.762.022 = **19.565.808** ✓ |
| Studio: intra + inter | 6.632.917 + 2.646.412 = **9.279.329** ✓ |
| Comuni di origine / destinazione (lavoro) | 7.904 / 7.903 |
| Primo flusso inter-comune | Guidonia Montecelio → Roma **17.299** |
| Polo con il saldo maggiore | Milano **+286.727** (384.744 entranti, 98.017 uscenti) |
| Comune con auto-contenimento minimo (pop>5.000) | Verderio (LC) **7,9%** |

## Un limite strutturale: i codici sardi

**394 comuni di origine non hanno nome** perché il codice 2021 non esiste nell'anagrafica
2026: 377 sono sardi (riforma provinciale, prefissi 090/091/092/095/111), gli altri sono
fusioni successive. Il mart li tiene con `in_anagrafica_2026 = false` e nome `NULL`, invece
di scartarli: valgono **216.023 uscenti (2,2%)** e includono il **6° flusso nazionale**
(092051 → 092009, Sassari, 9.501 pendolari).

Un join ingenuo su `codice_istat` contro l'anagrafica corrente perderebbe un'intera regione
in silenzio. Serve un crosswalk 2021 → 2026 prima della promozione.

## Criterio di promozione

- run verde con `toolkit` (2/2 mart, quality score 100)
- readiness 8/8
- crosswalk dei 394 codici prima di dichiarare il dataset completo

## Stato

- candidate implementato e verificato in locale (2026-11-23)
- issue di intake: #951

## Prossimo passo

- crosswalk anagrafica 2021 → 2026 (ISTAT "variazioni territoriali" o mappatura manuale dei
  394 codici)
- analysis: "Chi esce, chi entra, e dove" — mappa dei dormitori e dei poli
- il 2011 è disponibile (`DF_BULK_CPO2011_DICA_PEND`) ma con codici e perimetro diversi:
  eventuale confronto, non serie
