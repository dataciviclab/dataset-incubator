# bdap-lea

## Domanda guida

Quanto costa la sanità pubblica, ente per ente, e come si divide tra prevenzione,
assistenza distrettuale e assistenza ospedaliera?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / MEF.
**Modello LEA degli enti del SSN**, 13 annualità (2012-2024), CSV `;` in `cp1252`.

```
https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv
```

## Perimetro

- Annualità: **2012-2024** (13 anni).
- Granularità clean: una riga per **anno × ente × voce contabile**.
- Granularità mart: `mart_spesa_enti` per ente × voce; `mart_totale_ente` per
  ente × anno.

## Le due cose da sapere prima di sommare

**1. Le voci sono gerarchiche.** `1A100` contiene `1A110`, che contiene `1A111`.
Sommare le voci di dettaglio **moltiplica il totale per ~2,4** (verificato: ASL
TO3 2024, 2,77 mld di dettaglio contro 1,17 mld di totale reale). Per questo il
clean espone `tipo_voce`:

| `tipo_voce` | voci | si somma? |
|---|---|---|
| `totale` | `49999` (totale), `19999` prevenzione, `29999` distrettuale, `39999` ospedaliera, `48888` ricerca | **sì** |
| `dettaglio` | tutte le altre | **no** |

Identità verificata su 217/217 enti: `49999 = 19999 + 29999 + 39999 + 48888`.

**2. Ci sono tre tipi di riga.** Il clean espone `tipo_riga`:

| `tipo_riga` | codice | significato |
|---|---|---|
| `ente` | | azienda sanitaria (si somma tra loro) |
| `regione` | `000` | **ente regione**, soggetto reale |
| `consolidato` | `999` | totale regionale (include gli enti) |

La convenzione **000/999 è invertita** rispetto a quanto scritto nelle versioni
precedenti di questo README: `000` non è un aggregato, è l'ente regione. Il
double counting si evita escludendo `999`, non `000` (che è un soggetto).

## Numeri

Totale pubblicato (`49999`) degli enti, per anno:

| anno | enti | totale | prevenzione | distrettuale | ospedaliera |
|---|---:|---:|---:|---:|---:|
| 2012 | 272 | 137,7 mld | 4,8 | 65,8 | 67,1 |
| 2018 | 203 | 141,9 mld | 4,6 | 72,9 | 64,4 |
| 2024 | 217 | **174,2 mld** | 6,0 | 92,6 | 75,2 |

La prevenzione resta intorno al **3,5%** della spesa (6,0 mld su 174,2 nel 2024).
La crescita maggiore è nell'assistenza distrettuale (+41% dal 2012).

## Schema drift

La colonna `Oneri Finanziari` esiste solo in alcuni anni:

| anni | Oneri Finanziari |
|---|---|
| 2012-2018 | ❌ assente (22 colonne) |
| 2019 | ✅ |
| 2020 | ❌ |
| 2021-2022 | ✅ |
| 2023 | ❌ |
| 2024 | ✅ |

Gestito con `normalize_rows_to_columns` + `align_by_header`: le colonne assenti
diventano NULL invece di slittare le posizioni.

Attenzione anche alla **rottura di modello del 2019**: le voci passano da 121 a
109. I totali restano comparabili (`49999` esiste in tutti gli anni), ma il
dettaglio no: un'analisi per singola voce va verificata anno per anno.

## Schema

`clean` (25 colonne). Le principali:

| Colonna | Tipo | Ruolo |
|---|---|---|
| `anno_riferimento` | INTEGER | anno |
| `codice_regione`, `descrizione_regione` | VARCHAR | regione |
| `codice_ente_ssn`, `codice_ente_bdap`, `descrizione_ente` | VARCHAR | ente |
| `codice_voce_contabile`, `descrizione_voce_contabile` | VARCHAR | voce |
| `tipo_voce` | VARCHAR | `totale` / `dettaglio` |
| `tipo_riga` | VARCHAR | `ente` / `regione` / `consolidato` |
| `importo_totale` | DOUBLE | importo della voce |
| `oneri_finanziari` | DOUBLE | NULL negli anni senza la colonna |
| *(13 colonne metriche: consumi, prestazioni, servizi, personale, ammortamenti...)* | DOUBLE | componenti della voce |

## Mart

- **`mart_spesa_enti`**: ente × voce di dettaglio (stesso perimetro delle versioni
  precedenti: niente totali, niente `000`/`999`).
- **`mart_totale_ente`**: ente × anno con `totale` (49999), le quattro sezioni,
  `quadratura` (deve essere 0) e le quote di composizione.

## Run

```bash
toolkit run -c candidates/bdap-lea/dataset.yml
# 2012..2024: 13/13 run=ok validate=passed
```

Vedi `notes.md` per il dettaglio tecnico.
