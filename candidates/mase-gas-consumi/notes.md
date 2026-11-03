# Notes — mase_gas_consumi

## Fonte e accesso

Stessa fonte di `mase-gas-import` (MASE SISEN, API CMIS senza autenticazione).

- Cartella: `/sg_dgsaie/gas_naturale/consumi/`
- File usato: `Gas_Distribuito_Province_YYYY.xlsx` (2004-2025, 22 file)
- ID 2024: `0900fde8800c6a4f`

## Shape del file (verificato 2024)

Foglio `Foglio1`:

| Riga/col | Contenuto |
|---|---|
| A1-A3 | titolo / anno / unità |
| riga 5 | header: `REGIONE, PROVINCIA, INDUSTRIALE, [spacer], TERMOELETTRICO, RETI DI DISTRIBUZIONE, TOTALE GENERALE` |
| righe 6+ | province, **poi una riga `TOTALE ` per regione** con la regione in colonna A |

- `read.skip=4` + `header=true` → header = riga 5
- **Il nome regione sta in FONDO al blocco**, non in testa: le province di una regione
  sono quelle che *precedono* la sua riga `TOTALE`. Il clean risolve la regione con un
  `MIN(rn) OVER (ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)` sul prossimo nome non vuoto.
- La colonna spacer (D) è **sempre 0** → scartata.
- pandas legge **7 colonne** (A-G): le colonne H-O del foglio sono vuote.
- Le righe `TOTALE ` di regione sono escluse nel clean (110 province × 3 settori = 330 righe).

## Controlli di coerenza (2024)

- Somma dei settori per provincia = colonna `TOTALE GENERALE` del file ✓
- Somma delle province per regione = riga `TOTALE` regionale del file (es. PIEMONTE
  1.052,2 / 6.535,1 M Sm³) ✓
- Totale nazionale 3 settori = **60.830,6 M Sm³**, identico al TOTALE del file regionali ✓

## Insidie

- Formati misti: `.xls` (2004-2015) vs `.xlsx` (2016+) → due engine (xlrd/openpyxl)
- Anni recenti hanno `_old` o revisioni in altre cartelle (vedi `consumi_petroliferi`)
- Il file `consumi/regionali/` è **ridondante**: le regioni si ricavano dalle province
- Il file `consumi/annuali/` (`Consumi_gas_YYYY.xls`) è un'altra cosa — vendite mensili
  nazionali per settore — e **si ferma al 2014** (12 file, 2003-2014)

## Multi-anno (next step)

Come per `mase-gas-import`: la fonte espone un file per anno con ID non deterministico.
Per il multi-anno serve una `raw` di tipo `script` che enumera
`GET /cmis/documents?folder=/sg_dgsaie/gas_naturale/consumi/provinciali` e scarica ogni file.

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima della pubblicazione sull'Explorer.
