# elezioni-referendum

Risultati dei referendum abrogativi e costituzionali in Italia per comune e quesito (1995-2022).

**Fonte**: Eligendo — Archivio storico elettorale del DAIT (Ministero dell'Interno)
**Licenza**: dati pubblici

## Domanda guida

Come ha votato l'Italia nei referendum? Quali territori hanno votato SI o NO e come è cambiata la partecipazione?

## Dataset

- **Copertura**: 1995–2022 (12 tornate, 41 quesiti)
- **Granularità**: provinciale (1995-2006), comunale (2011-2022)
- **Righe**: ~100.000
- **Colonne**: 14 (data_elezione, regione, provincia, comune, elettori, votanti, voti_si, voti_no, ...)

## Schema (14 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `data_elezione` | DATE | Data del voto |
| `regione` | VARCHAR | Regione |
| `provincia` | VARCHAR | Provincia (solo 2011-2022: comune) |
| `comune` | VARCHAR | Comune (NULL per 1995-2006: dati provinciali) |
| `elettori` / `elettori_uomini` | BIGINT | Elettori |
| `votanti` / `votanti_uomini` | BIGINT | Votanti |
| `voti_si` / `voti_no` | BIGINT | Voti |
| `schede_*` | BIGINT | Nulle, bianche, contestate |
| `num_quesito` | BIGINT | Numero quesito |

## Mart analitici

| Mart | Granularità | Cosa produce |
|---|---|---|
| `mart_voti_quesito_comune` | comune × quesito | Voti SI/NO, affluenza%, pct_si, pct_no, esito |
| `mart_trend` | regione × anno | Trend affluenza referendaria (solo 2011-2022) |

## Dati salienti

| Tornata | Quesiti | Affluenza media | Quorum |
|---|---|---|---|
| 2011 | 4 | 57.5% | 4/4 raggiunto |
| 2016 | 1 (trivellazioni) | 49.1% | NON raggiunto |
| 2020 | 1 (taglio parlamentari) | 56.6% | NON raggiunto (valido per costo) |
| 2022 | 5 | 20.1% | NON raggiunto |

**Crollo affluenza**: da 57.5% (2011) a 20.1% (2022) — -37 punti in 11 anni. Il calo maggiore in Trentino-Alto Adige (-52pt), il minore in Sicilia (-29pt).

## Note

- **1995-2006**: solo granularità provinciale (comune = NULL)
- **2011-2022**: granularità comunale completa
- `mart_trend`: legge da tutti i clean parquet locali via glob (`{root}/data/clean/elezioni_referendum/*/...`). Non serve manutenzione: ogni nuovo anno runnato entra automaticamente.

## Stato

`candidate` — run verificato su tutte le 12 tornate.
