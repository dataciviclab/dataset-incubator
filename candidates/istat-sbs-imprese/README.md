# ISTAT SBS — Imprese per settore NACE

## Domanda

- Quali settori NACE generano più valore aggiunto, occupazione e investimenti in Italia?
- Quanto valore resta al lavoro e quanto al capitale?
- Come cambiano produttività per ora e costo del lavoro per ora?

## Dataset

- fonte: ISTAT via DBnomics (`type: dbnomics`)
- dataflow nazionale: `161_267_DF_DCSP_SBSNAZ_1`
- dataflow regionale: `161_268_DF_DCSP_SBSREG_1`
- copertura: **2008–2024**
- grano: Italia + 21 regioni NUTS1 × NACE sezioni B–S; livello nazionale esteso a NACE 10/11/12/47 per le filiere
- unità: **migliaia di euro** (`valore / 1000 = mln €`), **migliaia di ore**, conte
- dimensioni fissate: `PERS_EMPL_SIZE_CLASS=TOTAL`, `TURNOVER_CLASS=9`, `ENVIROM_DOMAIN=9`

## Indicatori

| Codice | Indicatore | Unità | Uso |
|---|---|---|---|
| `12110` | Fatturato | migliaia € | Margini, dimensione |
| `12120` | Valore della produzione | migliaia € | Produzione |
| `12150` | Valore aggiunto al costo fattore | migliaia € | Produttività, quota lavoro |
| `12170` | Risultato lordo di gestione | migliaia € | Proxy di redditività (GOS/VA) |
| `13310` | Costi del personale | migliaia € | Quota lavoro, ULC |
| `13320` | Salari e stipendi | migliaia € | Costo del lavoro, confronto INPS |
| `13330` | Contributi sociali | migliaia € | Costo azienda vs netto |
| `15110` | Investimenti fissi lordi | migliaia € | Investimenti/VA |
| `16150` | Ore lavorate dai dipendenti | migliaia ore | Produttività oraria, costo orario |
| `11110` | Imprese | conte | Numerosità |
| `11210` | Unità locali | conte | Numerosità |

## Copertura nazionale vs regionale

- **Nazionale**: tutti gli indicatori tranne `11210` (unità locali, disponibile solo a livello regionale), 2008–2024.
- **Regionale**: set lean (`12110`, `12150`, `13310`, `13320`, `11210`). Alcune serie regionali sono più corte o non disponibili nel dataflow regionale (es. ore lavorate, GOS, contributi sociali, investimenti dopo il 2015). Il livello nazionale è quello da usare per la matrice settoriale completa.

## Filiere agroalimentari

Il livello nazionale include anche i codici NACE a 2 cifre utili al quadro filiera:

- `10` industria alimentare
- `11` industria delle bevande
- `12` industria del tabacco
- `47` commercio al dettaglio

SBS **non copre l'agricoltura** (`A`/`01`): per il primo stadio della filiera
usare RICA. `mart_sbs_filiere` è la matrice dedicata; `mart_sbs_settore` resta
sulle sezioni.

## Perché vale la pena

- **Ore + costi del personale + VA** permettono di calcolare produttività per ora, costo del lavoro per ora, quota lavoro e costo del lavoro per unità di valore aggiunto — con unità coerenti.
- **GOS** aggiunge un proxy di redditività, più solido del solo margine IVA.
- **Investimenti** permettono di leggere il rapporto investimenti/VA per settore.
- **Classi dimensionali e quartili** (follow-up) permettono di studiare eterogeneità dentro i settori senza bilanci firm-level.

## Output

- `mart_sbs_anno`: `anno × territorio × grain × NACE × indicatore` con `valore` e `unita_misura` (long format, nazionale + regionale).
- `mart_sbs_filiere`: matrice nazionale `anno × NACE` per `10/11/12/47`, con VA, costo del lavoro, salari, contributi, GOS, investimenti, ore, imprese e indicatori derivati.
- `mart_sbs_settore`: matrice nazionale `anno × NACE` (wide, sole sezioni) con VA, costo del lavoro, salari, contributi, GOS, investimenti, ore e indicatori derivati:
  - `va_per_ora_eur`, `costo_lavoro_per_ora_eur`, `salario_per_ora_eur`
  - `quota_lavoro_pct`, `gos_su_va_pct`, `investimenti_su_va_pct`
  - `salari_su_costo_lavoro_pct`, `contributi_su_costo_lavoro_pct`

La matrice è il contratto pronto per l’analisi settoriale; il long format resta la base per altri usi e per il livello regionale.

## Limiti

- **Copertura**: SBS copre industria, costruzioni, commercio e servizi di mercato; **finanza (K) e PA (O) non sono coperte**. Per quei settori usare Eurostat GVA/occupazione.
- **GOS non è profitto netto**: è un risultato lordo, prima di interessi, tasse e dividendi.
- **Ore lavorate = dipendenti**: non includono gli autonomi; non sono ore effettive, ma ore lavorate dichiarate.
- **Costi del personale** includono salari e contributi sociali, non solo retribuzioni nette.
- **Dati survey**: non sono bilanci firm-level; per quello servono AIDA/Cerved/Registro Imprese XBRL.
- **Agricoltura assente**: SBS non copre `A`/`01`; il dettaglio filiera è trasformazione (10/11/12) e retail (47), non produzione agricola.
- **2024** può essere provvisorio.

## Run

```bash
cd candidates/istat-sbs-imprese
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```
