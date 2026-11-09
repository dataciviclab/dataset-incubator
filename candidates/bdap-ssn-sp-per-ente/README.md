# bdap-ssn-sp-per-ente

## Domanda guida

Quale azienda sanitaria ha i debiti? Lo Stato Patrimoniale regionale dice quanto
deve una regione; questo dice **quanto deve ogni singola ASL o azienda
ospedaliera**, e con quale patrimonio.

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / MEF.
**Modello di rilevazione dello Stato Patrimoniale degli enti del SSN** (livello
per ente), 13 package annuali, CSV `;` in `cp1252`, ~6,8 MB per anno.

```
https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv
```

## Perimetro

- Annualità: **2012-2024** (13 anni).
- Granularità clean: una riga per **anno × ente × voce** (~36.000 righe/anno).
- Granularità mart: una riga per **anno × ente** (255 nel 2024).
- Contiene **tre tipi di riga**: enti, ente regione e consolidato regionale.

## Schema

`clean` (16 colonne):

| colonna | contenuto |
|---|---|
| `anno`, `codice_regione`, `descrizione_regione` | anagrafica |
| `codice_ente_ssn`, `codice_ente_bdap`, `descrizione_ente` | identità dell'ente |
| `tipo_riga` | `ente` / `regione` (codice `000`) / `consolidato` (`999`) |
| `codice_voce` / `descrizione_voce` | voce del prospetto |
| `prospetto`, `sezione`, `riga_sintesi` | attivo/passivo, sezione, totali di sezione |
| `livello` / `voce_livello1` | profondità (cifre romane: `A.I`, `A.I.1.a`) |
| `importo`, `data_aggiornamento` | importo e data dichiarata dalla fonte |

`mart_patrimonio_ente`: attivo, patrimonio netto, fondi rischi, TFR, debiti,
ratei, `utile_esercizio`, `quadratura`, quote su attivo.

## Attenzione: `tipo_riga`

| tipo | significato | come si usa |
|---|---|---|
| `ente` | azienda sanitaria (ASL, AO, IRCCS) | **si somma** tra loro |
| `regione` | ente regione (codice `000`): **soggetto reale**, non un aggregato | si tiene separato |
| `consolidato` | totale regionale (codice `999`) | **non si somma** agli altri |

La convenzione è **invertita** rispetto al modello LEA (`000` = aggregato, `999` =
ente regione): qui `000` è un'entità contabile vera. Chi riusa la regola del LEA
butta via l'ente regione e somma due volte.

## Numeri

| anno | enti | attivo enti | debiti enti | debiti ente regione | consolidato |
|---|---:|---:|---:|---:|---:|
| 2012 | 252 | 99,1 mld | 79,9 mld | 48,5 mld | 104,7 mld |
| 2018 | 204 | 80,3 mld | 39,5 mld | 44,2 mld | 96,6 mld |
| 2024 | 217 | 98,4 mld | **40,5 mld** | **49,5 mld** | **125,6 mld** |

Il debito delle aziende si è **dimezzato** (79,9 → 40,5), mentre quello delle
regioni è rimasto stabile: la riduzione del debito sanitario raccontata dal
dataset regionale è tutta lato aziende. Il numero di enti scende da 252 a 217:
fusioni e accorpamenti.

## Verifiche fatte sulla fonte

1. **Consolidato = dataset regionale**: la somma delle righe `999` coincide con
   `bdap_ssn_stato_patrimoniale` **su tutte le 13 annualità, scarto 0,0 mln**.
2. **Quadratura patrimoniale per ente**: attivo derivato = passivo derivato su
   **216/217 enti** nel 2024; unico scarto 34,2 mln (Sardegna, difetto noto).
3. **Chiave**: `(anno, codice_ente_bdap, codice_ente_ssn, codice_voce)` **unica**
   (36.097 righe, 0 duplicati nel 2024). Serve il codice SSN perché uno stesso
   ente BDAP può avere più codici SSN (es. INRCA: 916, 920, 921).
4. **Schema stabile** in tutti i 13 anni.

## Caveat

- **I totali generali pubblicati mancano** in molte righe (nel 2024 `AZZ999` c'è
  per 140 enti su 217): attivo e passivo sono derivati dalle sezioni, come nel
  dataset regionale.
- **`000` presente in 17 regioni su 21** nel 2024: in quattro regioni la riga
  dell'ente regione non è pubblicata.
- **Entità ambigue**: 236 codici BDAP, 238 denominazioni, 114 codici SSN. Lo
  stesso codice BDAP può comparire con più codici SSN e nomi diversi (presidi
  della stessa azienda): l'identità legale è il codice BDAP, l'unità contabile è
  la coppia `(bdap, ssn)`.
- **Ponte verso SIOPE**: il codice ente BDAP non ha lo stesso formato del codice
  SIOPE, ma il **codice fiscale** sì (verificato 149/149 enti sul Conto
  Economico). Per collegare questo dataset ai pagamenti SIOPE serve passare da
  `bdap_anagrafe_enti`.

Vedi `notes.md` per le scelte tecniche.
