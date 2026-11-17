# Notes — aifa_spesa_consumo

## Fonte e download

Pagina AIFA (open data): *Spesa e consumo relativi al flusso della farmaceutica
convenzionata e degli acquisti diretti*, aggiornata al 06/08/2026, copertura
**2016-2025**.

AIFA **non ha un template URL stabile**: fino al 2024 i file sono CSV diretti
con la data nel nome, dal 2025 diventa un ZIP. In `dataset.yml` c'è quindi una
sorgente per anno, con `year: YYYY` che la attiva solo sul proprio run.

| Anno | File | Formato | Righe raw |
|---|---|---|---:|
| 2016 | `dati2016_100519.csv` | CSV | 164.195 |
| 2017 | `dati2017_100519.csv` | CSV | 163.326 |
| 2018 | `dati2018_23.09.2020.csv` | CSV | 174.254 |
| 2019 | `dati2019_23.09.2020.csv` | CSV | 176.770 |
| 2020 | `dati2020_22.10.2021.csv` | CSV | 171.006 |
| 2021 | `dati2021_24.10.2022.csv` | CSV | 169.304 |
| 2022 | `dati2022_07.02.2024.csv` | CSV | 172.304 |
| 2023 | `dati2023_15.01.2025.csv` | CSV | 174.595 |
| 2024 | `dati2024_04.12.2025.csv` | CSV | 177.749 |
| 2025 | `dati_2025_260514.zip` | ZIP → 1 CSV | 177.635 |

Il ZIP del 2025 contiene un solo CSV (`dati_2025_260514.csv`, 31,9 MB): la
sorgente 2025 ha `extractor: unzip_first_csv`, le altre no.

## Encoding: cp1252, non UTF-8

Tutti i file contengono byte non-UTF-8. Dal 2024 sono `0xA0` (NBSP), nel 2016
anche `0x92` (apostrofo tipografico in Windows-1252). Quindi:

- `utf-8` fallisce già alla riga 148 del 2016;
- `latin-1` **non basta**: DuckDB rifiuta il file perché `0x92` non è valido in
  ISO-8859-1;
- `cp1252` funziona su tutti gli anni.

Il match è forzato con `read.encoding: "cp1252"` e `read.all_varchar: true`
(evita che lo sniffing tipizzi `codreg`, perdendo lo zero iniziale).
`ignore_errors` è stato rimosso: era il modo in cui i byte sporchi sparivano
senza segnalarlo.

**NBSP nelle descrizioni.** La fonte mette `0xA0` in testa/coda a
`descrizione_atc3`/`descrizione_atc4` (247 righe nel 2025, 250 nel 2016). `TRIM`
non lo toglie, quindi `clean.sql` fa `replace(x, chr(160), ' ')` prima di
normalizzare. Senza questo, le descrizioni restano "sporche" di un carattere
invisibile.

## Deroga `primary_key` sul clean

`clean.validate.primary_key` **non è dichiarata**, ed è una deroga esplicita.

Motivo: 2016 e 2017 hanno più righe con la stessa
`(anno, mese, codreg, classe, atc4)` e importi diversi. La fonte non espone la
dimensione che le distingue.

| Anno | Righe | Chiavi distinte | Duplicati |
|---|---:|---:|---:|
| 2016 | 164.195 | 162.899 | 1.290 gruppi |
| 2017 | 163.326 | 163.304 | 22 gruppi |
| 2018-2025 | — | — | 0 |

Esempio 2016 (Piemonte, gennaio, A03FA): una riga `1 conf. / 9,34 €` e una
riga `25 conf. / 158,35 €`, stesse descrizioni. Sommarle è corretto — è quello
che fa il mart nel `GROUP BY`, dove la chiave torna univoca.

## Righe senza ATC

Poche righe reali non hanno `classe`/`atc4` ma hanno i volumi del flusso
tracciabilità (10 nel 2021, 41 nel 2023, 1 nel 2022). Non sono righe vuote:
non vanno scartate. Per questo `not_null` copre solo `anno`, `mese`, `codreg`.

## Flusso convenzionata

Il mart analizza **solo** la convenzionata. Dal 2016 la fonte contiene anche
righe di sola tracciabilità (`spesa_convenzionata` NULL):

| Anno | Righe clean | Con convenzionata |
|---|---:|---:|
| 2016 | 164.195 | 97.889 |
| 2019 | 176.770 | 92.711 |
| 2024 | 177.749 | 92.225 |
| 2025 | 177.635 | 90.970 |

Il clean è raw-faithful e le tiene tutte; il mart filtra
`spesa_convenzionata IS NOT NULL`.

## Numeri della serie (convenzionata)

| Anno | Spesa (mln €) | Confezioni (mln) | € / confezione |
|---|---:|---:|---:|
| 2016 | 10.638,0 | 1.117,7 | 9,52 |
| 2017 | 10.494,8 | 1.109,2 | 9,46 |
| 2018 | 10.139,7 | 1.101,6 | 9,20 |
| 2019 | 10.087,5 | 1.085,3 | 9,29 |
| 2020 | 9.820,4 | 1.035,3 | 9,49 |
| 2021 | 9.772,3 | 1.030,8 | 9,48 |
| 2022 | 9.880,5 | 1.040,1 | 9,50 |
| 2023 | 9.872,2 | 1.036,3 | 9,53 |
| 2024 | 10.031,8 | 1.041,7 | 9,63 |
| 2025 | 10.514,3 | 1.037,9 | 10,13 |

**Attenzione alla frase "spesa stabile".** Sul 2018-2024 è stabile in valore
nominale (~10,0 mld). Sulla serie intera 2016-2025 cala del **−1,2%** (CAGR
−0,14%), con minimo nel 2021 e recupero dal 2023. Nel 2025 è **+4,8% sul
2024**, e il costo medio per confezione sale a 10,13 € (+6,4% sul 2016).
In termini reali la spesa è calata: serve un deflatore prima di parlare di
crescita.

## Mart

1. `mart_mensile_regione_atc4` — anno × mese × regione × classe × ATC4.
   Granularità del dataset. Chiave: `[anno, mese, codreg, classe, atc4]`.
2. `mart_sintesi_regione_anno` — regione × anno, con costo medio per confezione,
   quota nazionale e rank regionale del costo medio.
3. `mart_trend_regione` — una riga per regione sull'intera serie: delta %,
   CAGR e costo medio dell'ultimo anno. Legge tutti gli anni via glob, quindi
   il risultato non dipende dall'anno del run.

## Quirk noti

- `url_suffix_by_year` **non funziona** per il 2025 (naming cambiato) e il
  preflight non lo applicherebbe comunque: per questo la sorgente è esplicita
  per anno.
- Il preflight di toolkit controlla l'URL base senza `url_suffix_by_year`:
  su questa fonte dà falsi negativi. Non blocca il run.
- Il "Manuale Operativo" linkato da AIFA puntava a un CV Europass (link rotto):
  lo schema è stato ricostruito dai file reali.
