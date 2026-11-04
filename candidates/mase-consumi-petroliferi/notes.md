# Notes — mase_consumi_petroliferi

## Fonte e accesso

Stessa fonte degli altri candidate MASE (SISEN, API CMIS pubblica, nessuna auth).

- Cartella usata: `consumi_petroliferi/definitivi` — `Consumi_Petroliferi_Definitivi_YYYY.xls(x)`,
  **2002-2025**, 24 file
- `consumi_petroliferi/preconsuntivi/{anno}/` (`Consumi_Petrolio_YYYY_MM.xls`) è un'altra
  forma (mensile con confronto anno precedente + YTD): **fuori dal v0**

## Layout (stabile; variano foglio, formato e righe di titolo)

```
riga titolo   CONSUMI PETROLIFERI  ANNO YYYY
riga          I° SEMESTRE                       2°SEMESTRE
riga header   PRODOTTO | <dett> | GEN. | FEB. | GEN.FEB | …   PRODOTTO | <dett> | LUG. | …
righe dati    BENZINA | AUTO TOTALE | 652 | 620 | 1272 | …    BENZINA | AUTO TOTALE | 873 | …
```

- Due blocchi affiancati (I°/II° semestre), ciascuno con la propria colonna PRODOTTO
- Colonne mese (0-based): `2,3,5,7,9,11` (GEN..GIU) e `15,17,19,21,23,25` (LUG..DIC).
  Le colonne **cumulative** (`GEN.FEB`, `GEN.MAR`, …) sono ignorate.
- Il nome prodotto è solo sulla prima riga del blocco; le righe successive hanno
  celle vuote o i marcatori `DI CUI:` / `=` → forward-fill che li ignora
- **Il parser individua la riga di intestazione** (cerca `PRODOTTO` + una cella `GEN*`)
  invece di assumere un offset: l'offset cambia tra le ere (riga 3 nel 2002, riga 4 dal 2020)

## Insidie risolte

### Anno dal titolo, non dal nome file
Alcuni file contengono **più anni in fogli diversi**:
`Consumi_Petroliferi_Definitivi_2023.xlsx` ha 3 fogli → 2021, 2022, 2023.
Il preprocess legge l'anno dal **titolo del foglio** e tiene solo le righe dell'anno
del file, scartando i fogli extra (loggato a ogni run).

### Etichette prodotto variabili
| Etichetta grezza | Canonica |
|---|---|
| `CARBOT.` / `CARBOTURBO` | carboturbo |
| `OLIO COMB.` / `OLIO COMB.LE` / `OLIO COMBUSTIBILE` | olio combustibile |
| `G.P.L.` / `GPL` | gpl |
| `LUBRIFICANTI TOTALE` | lubrificanti |
| `TOTALE PRODOTTI PRINCIPALI` | totale prodotti principali |

E le varianti della riga di totale (`TOTALE`, `TOTALE (A)`, `TOTALE GASOLI`,
`T O T A L E`) sono allineate a `TOTALE`. I marcatori di nota `(*)` sono rimossi
(`BENZINA(*)` → `BENZINA`).

## Controlli di coerenza

- 2025: benzina 8.937 kt, gasolio 25.799 kt → coincidono col foglio (`GEN.DIC`) ✓
- 24 anni × 8 prodotti × 12 mesi = **2.304 righe** clean ✓
- `SUM(quota_pct)` = 100 per ogni anno ✓

## Insidie residue

- Le ripartizioni "di cui" (rete/extrarète, autotrazione, termoelettrica) sono nel
  raw ma non selezionate dal clean: disponibili per un'estensione
- `min_rows` va rivisto se si aggiungono anni

## Licenza

Non dichiarata sul portale MASE. Da chiarire prima della pubblicazione sull'Explorer.
