# bdap-ssn-conto-economico

## Domanda guida

Quanto costa la sanità pubblica regione per regione, e come si compone quel costo
(personale, beni, servizi)? Quanto pesa il finanziamento indistinto rispetto ai
ricavi propri?

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / MEF.
Modello di rilevazione del **Conto Economico degli enti del SSN a livello Regionale**.
Catalogo CKAN `openbdap`, 13 package (uno per annualità), CSV `;` in `cp1252`.

```
https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv
```

Gli UUID per anno sono in `dataset.yml` (`url_suffix_by_year`).

## Perimetro

- Annualità: **2012-2024** (13 anni), tutti i territori presenti nella fonte.
- Granularità clean: una riga per **anno × regione × voce di conto**.
- Granularità mart: una riga per **anno × regione**.
- Valori in **euro** (non deflazionati), come pubblicati dalla fonte.

## Schema

`clean` (11 colonne, ~8k righe/anno):

| colonna | contenuto |
|---|---|
| `anno` | anno di riferimento |
| `codice_regione` / `descrizione_regione` | 21 territori (19 regioni + PA Bolzano + PA Trento) |
| `codice_voce` | codice BDAP della voce (es. `AA0010`, `BZ9999`) |
| `descrizione_voce` | descrizione con prefisso gerarchico (`A.1)`, `A.9.B)`) |
| `sezione` | `A` ricavi, `B` costi, `C` finanziari, `D` rettifiche, `E` straordinari, `Y` imposte, `Z` risultato |
| `riga_sintesi` | `true` per i totali di sezione (`*Z9999`) |
| `livello` | profondità gerarchica (1 = `A.1`, 2 = `A.9.B`, ...), `null` per le righe di sintesi |
| `voce_livello1` | prima voce di livello 1 a cui appartiene (`A.1`, `B.5`, ...) |
| `importo` | importo in euro |
| `data_aggiornamento` | data di aggiornamento dichiarata dalla fonte |

`mart` (`mart_composizione_regionale`): `contributi_esercizio`, `ricavi_prestazioni`,
`ticket`, `totale_ricavi`, `acquisti_beni`, `acquisti_servizi`, `manutenzione`,
`godimento_beni_terzi`, le quattro voci del personale, `costo_personale`,
`oneri_diversi`, `totale_costi`, `risultato_esercizio`, più due quote
(`quota_personale_su_costi`, `quota_contributi_su_ricavi`).

## Numeri chiave

| anno | ricavi (mld €) | costi (mld €) | risultato (mld €) |
|---|---:|---:|---:|
| 2012 | 119,5 | 115,6 | +0,89 |
| 2016 | 120,1 | 117,8 | −0,28 |
| 2020 | 132,8 | 130,2 | +0,09 |
| 2024 | 150,0 | 149,2 | −0,85 |

2024: costo del personale **40,4 mld €** (27% dei costi), contributi in c/esercizio
**135,4 mld €** (90% dei ricavi).

## Verifiche fatte sulla fonte

1. **Identità di bilancio**: `ZZ9999 = AZ9999 − BZ9999 + CZ9999 + DZ9999 + EZ9999 − YZ9999`
   → scarto **0,00 €** su 21/21 territori in 2012 e 2024.
2. **Quadratura di sezione**: `AZ9999` = somma delle voci `A.N` di primo livello
   → 21/21 territori in 2012 e 2024.
3. **Regionale = nazionale**: somma dei 21 bilanci regionali 2024 = file
   "Conto Economico SSN a livello Nazionale" 2024 (150,05 / 149,20 / −0,85 mld €).
4. **Serie**: 13/13 anni con `readiness: ready`, schema stabile (stesse 7 colonne
   in tutti gli anni).

## Caveat

- **Calabria assente nel 2021**: il file sorgente non contiene righe per `180`.
  Non è un errore di pipeline; il 2021 ha 20 territori invece di 21.
- **Mobilità sanitaria**: `ricavi_prestazioni` e i costi corrispondenti sono
  transazioni tra aziende. A livello nazionale si compensano, a livello regionale
  no: non leggere la somma regionale dei ricavi come "spesa sanitaria delle regioni".
- **Voci contabili**: la numerazione nella descrizione cambia tra anni
  (`B.10`–`B.16` nel 2012, `B.10`–`B.14` nel 2024); i codici delle voci principali
  sono invece stabili, ed è su quelli che è costruito il mart.
- **Gerarchia nella descrizione, non nel codice**: `livello` e `voce_livello1`
  sono derivati dal prefisso testuale. Le righe di sintesi (`*Z9999`) non hanno
  prefisso e hanno `livello = null`.

## Prossimi passi

- Aggiungere le altre due famiglie dello stesso modello (Conto Economico livello
  **nazionale**, **Stato Patrimoniale** regionale e nazionale).
- Pro-capite per regione richiede un join con la popolazione (dataset esterno).

Vedi `notes.md` per il dettaglio del source-check e delle scelte di mapping.
