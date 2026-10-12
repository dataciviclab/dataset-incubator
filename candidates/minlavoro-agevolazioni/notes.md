# Notes — minlavoro-agevolazioni

## Quirk della fonte

- **API OData instabile**: stessa nota di minlavoro-flussi — User-Agent obbligatorio, retry necessari. Cache locale in `data/` (gitignored).
- **Tabelle eterogenee**: le 6 tabelle hanno schemi diversi (regione×mese, regione×tipologia, solo obiettivi). L'extract le fonde in uno schema long con campi nullable.
- **Anno non sempre presente**: 3 tabelle cross-section non hanno colonna Anno (`altre_agevolazioni`, obiettivi decontribuzione, contratti attivi detassazione — 268 righe). Il clean le esclude (`anno IS NOT NULL`); la serie storica parte dal 2016.
- **Indicatori multipli**: `Dichiarazioni`, `Num. di dichiarazioni`, `Num. contratti attivi` — i mart filtrano per quelli conteggio.

## Decisioni metodologiche

- **tipologia_contratto / categoria / settore come campi nullable**: non tutte le tabelle hanno tutte le dimensioni. Lo schema long le rende tutte opzionali.
- **Solo decontribuzione e detassazione nei mart**: le altre agevolazioni (omnicomprensività ecc.) hanno volumi bassi e non hanno serie storica.
- **Filtro anno NOT NULL nel clean**: le tabelle cross-section senza serie storica non producono righe utili ai mart; escluirle evita righe con anno NULL nelle aggregazioni.
- **primary_key deroga (clean)**: non dichiarata — tabelle eterogenee con dimensioni parziali. PK dichiarate nei mart.

## Rischi noti

- Le tabelle cross-section (contratti attivi per obiettivi, altre agevolazioni) non hanno serie storica.
- La serie 2024 potrebbe essere parziale (deposito ancora in corso).
- Fonte con WAF: rate-limit possibile in CI.

## Join con minlavoro-flussi

```sql
-- ROI agevolazioni → attivazioni per regione × anno
SELECT a.regione, a.anno,
       a.n_dichiarazioni AS agevolazioni,
       f.n_rapporti AS attivazioni
FROM mart_agevolazioni_regione a
JOIN mart_flussi_regione f
  ON a.regione = f.territorio AND a.anno = f.anno
WHERE f.tipo_flusso = 'attivazione'
```
