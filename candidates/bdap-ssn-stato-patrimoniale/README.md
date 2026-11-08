# bdap-ssn-stato-patrimoniale

## Domanda guida

Quanto possiedono e quanto devono le aziende sanitarie, regione per regione? Il
Conto Economico dice *quanto costa* la sanità; questo dice *con quali debiti e
quale patrimonio* la si finanzia.

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / MEF.
**Modello di rilevazione dello Stato Patrimoniale degli enti del SSN a livello Regionale**,
13 package (uno per annualità), CSV `;` in `cp1252`.

```
https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv
```

## Perimetro

- Annualità: **2012-2024** (13 anni), 21 territori.
- Granularità clean: una riga per **anno × regione × voce** (281 voci).
- Granularità mart: una riga per **anno × regione**.
- Valori in **euro**, come pubblicati.

## Schema

`clean` (12 colonne, ~4.000 righe/anno):

| colonna | contenuto |
|---|---|
| `anno`, `codice_regione`, `descrizione_regione` | anagrafica |
| `codice_voce` / `descrizione_voce` | voce del prospetto (es. `AAZ999`, `PAA220`) |
| `prospetto` | `attivo` / `passivo` (dal primo carattere del codice) |
| `sezione` | primi due caratteri (`AA` immobilizzazioni, `AB` attivo circolante, `PA` patrimonio netto, `PD` debiti, ...) |
| `riga_sintesi` | `true` per i totali di sezione (`*Z999`) |
| `livello` / `voce_livello1` | profondità e voce di primo livello (numerazione a cifre romane: `A.I`, `A.I.1.a`) |
| `importo` | importo in euro |
| `data_aggiornamento` | data dichiarata dalla fonte (stringa `gg/mm/aaaa`) |

`mart_patrimonio_regionale`: `attivo`, `patrimonio_netto`, `fondi_rischi`, `tfr`,
`debiti`, `ratei_attivi/passivi`, `passivo`, `utile_esercizio`, più i controlli
`quadratura` (attivo − passivo derivati) e i totali pubblicati dalla fonte.

## Numeri

| anno | attivo | patrimonio netto | debiti |
|---|---:|---:|---:|
| 2012 | 104,7 mld | 20,7 mld | **72,4 mld** |
| 2018 | 96,6 mld | 32,4 mld | 44,8 mld |
| 2024 | 125,6 mld | 46,4 mld | **49,1 mld** |

Il debito delle aziende sanitarie è sceso di **23 mld** in dodici anni, mentre il
patrimonio netto è più che raddoppiato.

2024, debiti per regione:

| regione | debiti | % dell'attivo |
|---|---:|---:|
| Lombardia | 12,08 mld | 43,0% |
| Sicilia | 8,39 mld | 58,7% |
| Lazio | 3,98 mld | 37,8% |
| Emilia-Romagna | 3,46 mld | 44,4% |
| Campania | 2,90 mld | 27,9% |

## Verifiche fatte sulla fonte

1. **Quadratura patrimoniale**: attivo derivato = passivo derivato. Dal 2020 lo
   scarto è **0,00** su tutte le regioni; nel 2024 solo la **Sardegna** non quadra
   (+34,2 mln) e 2012-2015 hanno scarti fino a 222 mln.
2. **Coerenza con il Conto Economico**: `PAA220` (utile d'esercizio) = `ZZ9999`
   del CE. Scarto 0 su 2020 e 2022-2024; differenze da revisione della fonte su
   Sardegna 2012-2015; **Calabria 2021 non confrontabile** perché il CE non ha
   quella regione (gap noto della fonte).
3. **Schema stabile**: stesse 7 colonne in tutti i 13 anni, 21 regioni.

## Caveat

- **I totali generali pubblicati non sono affidabili**: `AZZ999` (D. Totale attivo)
  manca in 9 regioni nel 2024, in 11 nel 2020 e in **tutte** nel 2012. Il mart
  deriva attivo e passivo dalla somma delle sezioni; il totale pubblicato è
  conservato solo come colonna di controllo.
- **Conti d'ordine esclusi** dai totali: sono voci di memo (garanzie, impegni),
  non attività o passività patrimoniali.
- **La Sardegna non quadra nel 2024** (34,2 mln): è un difetto della fonte, non
  del clean.
- **Nessuna chiave per ente**: questo file è aggregato regionale. Il livello
  per-ente esiste in un'altra famiglia (vedi `notes.md`).

Vedi `notes.md` per le scelte tecniche e il ponte verso il livello per-ente.
