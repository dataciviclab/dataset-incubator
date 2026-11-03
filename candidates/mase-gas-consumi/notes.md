# Notes — mase_gas_consumi

## Fonte e accesso

Stessa fonte di `mase-gas-import` (MASE SISEN, API CMIS pubblica, nessuna auth).

- Cartella: `/sg_dgsaie/gas_naturale/consumi/provinciali`
- File: `Gas_Distribuito_Province_YYYY.xls(x)` — **2004-2025**, 22 file
- Niente download per nome/path → serve il `script` (come per `mase-gas-import`)

## Layout (stabile, cambiano solo foglio e formato)

| Era | Foglio |
|---|---|
| 2004-2015 `.xls` | `GAS_PROVINCIA` |
| 2016+ `.xlsx` | `Foglio1` |

Struttura:

```
riga 1-2   titolo + ANNO YYYY
riga 3     unità
riga 5     REGIONE | PROVINCIA | INDUSTRIALE | <spacer> | TERMOELETTRICO | RETI | TOTALE GENERALE
riga 6+    province (colonna REGIONE vuota)
           ... poi una riga TOTALE per regione, con la regione in colonna 0
```

- **Il nome regione sta in fondo al blocco**, non in testa: le province di una
  regione sono quelle che *precedono* la sua riga `TOTALE`. `preprocess.py`
  accumula il blocco e lo chiude alla riga `TOTALE`.
- La colonna spacer (indice 3) è **sempre 0** → scartata.
- Riga di fonte a piè di foglio (`MINISTERO DELLO SVILUPPO ECONOMICO - …`):
  esclusa sia per prefisso sia perché senza valori.

## Controlli di coerenza

- 2024: somma province = **60.831 M Sm³** = `TOTALE GENERALE` del file ✓
- Somma province per regione = riga `TOTALE` regionale (es. PIEMONTE 6.535,1) ✓
- 2.364 righe grezze (wide) → 7.048 nel clean (unpivot 3 settori)

## Perché non c'è il file regionale

`consumi/regionali/` (`Gas_Distribuito_Regioni_YYYY.xls`, 24 file) è **ridondante**:
le regioni si ricavano dalle province, e il mart `mart_consumo_regione` lo fa.

`consumi/annuali/` (`Consumi_gas_YYYY.xls`, 12 file) è un'altra cosa — vendite
mensili nazionali per settore — e **si ferma al 2014**.

## Insidie

- Il numero di province varia nel tempo (102/104/106/110): riorganizzazioni
  amministrative (Sardegna, province soppresse). Non è un buco.
- I nomi provincia possono variare leggermente tra anni: vanno verificati su
  un aggiornamento (es. accenti)
- La soglia `min_rows` va rivista se si aggiungono anni

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima della pubblicazione sull'Explorer.
