# bdap-ssn-ce-per-ente

## Domanda guida

Quale azienda sanitaria perde, e quanto? Il Conto Economico regionale dice il
risultato di una regione; questo dice il risultato di **ogni ASL, azienda
ospedaliera e IRCCS**, con la composizione dei costi.

## Fonte

OpenBDAP — Ragioneria Generale dello Stato / MEF.
**Modello di rilevazione del Conto Economico degli enti del SSN** (livello per
ente, package annuale), 13 annualità, CSV `;` in `cp1252`, ~76.000 righe/anno.

```
https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv
```

## Perimetro

- Annualità: **2012-2024** (13 anni).
- Granularità clean: una riga per **anno × ente × voce** (554 voci nel 2024).
- Granularità mart: una riga per **anno × ente**.
- Include **tre tipi di riga**: enti, ente regione e consolidato regionale.
- I package **trimestrali** sono esclusi (vedi `notes.md`).

## Schema

`clean` (16 colonne):

| colonna | contenuto |
|---|---|
| `anno`, `codice_regione`, `descrizione_regione` | anagrafica |
| `tipo_rilevazione` | dichiarato dalla fonte (`CONSUNTIVO`) |
| `codice_ente_ssn`, `codice_ente_bdap`, `descrizione_ente` | identità dell'ente |
| `tipo_riga` | `ente` / `regione` (`000`) / `consolidato` (`999`) |
| `codice_voce`, `descrizione_voce` | voce del CE (es. `AA0010`, `BZ9999`) |
| `sezione` | `A` ricavi, `B` costi, `C` finanziari, `D` rettifiche, `E` straordinari, `Y` imposte, `Z` risultato |
| `riga_sintesi` | `true` per i totali da non sommare: sezioni (`*Z9999`) e subtotali `XA0000`/`BA2080`/`BA2560` |
| `livello`, `voce_livello1` | profondità e voce di primo livello (cifre arabe: `A.1`, `B.5`); **NULL sulle righe di sintesi** |
| `importo`, `data_aggiornamento` | importo e data dichiarata |

`mart_conto_economico_ente`: stesse misure del dataset regionale —
`contributi_esercizio`, `ricavi_prestazioni`, `ticket`, `totale_ricavi`,
`acquisti_beni`, `acquisti_servizi`, le quattro voci del personale,
`costo_personale`, `totale_costi`, `risultato_esercizio`, più le due quote.

## Attenzione: qui ricavi e costi NON sono additivi

| 2024 | ricavi | costi | risultato |
|---|---:|---:|---:|
| enti (217) | 170,3 mld | 170,9 mld | −2,59 mld |
| ente regione (15) | 7,0 mld | 5,5 mld | +1,74 mld |
| **consolidato** | **150,1 mld** | **149,2 mld** | **−0,85 mld** |

Sommare i ricavi degli enti al consolidato **gonfia il totale di ~20 mld**: le
aziende si scambiano prestazioni (mobilità sanitaria) e ricevono trasferimenti
dalla regione, flussi che il consolidato elimina. Il **risultato** invece quadra
(`000` + enti ≈ `999`).

Regola: **i volumi si leggono solo nel consolidato; il per-ente serve per
confrontare e per il risultato.** Nello Stato Patrimoniale questa trappola non
c'era: lì attivo e passivo quadravano per ente.

Nota sulle voci: `riga_sintesi` marca i totali da non sommare — i totali di
sezione (`*Z9999`) più i subtotali che la fonte pubblica senza codice Z
(`XA0000` risultato ante imposte, `BA2080` costo del personale, `BA2560`
ammortamenti). Su quelle righe `livello` e `voce_livello1` sono NULL per
costruzione: il resto del dataset è coperto al 100%.

## Numeri

| anno | enti | ricavi enti | risultato enti | risultato ente regione | consolidato |
|---|---:|---:|---:|---:|---:|
| 2012 | 254 | 131,4 mld | −1,28 mld | +2,20 mld | **+0,89 mld** |
| 2018 | 204 | 141,7 mld | −1,03 mld | +0,93 mld | −0,11 mld |
| 2024 | 217 | 170,3 mld | **−2,59 mld** | +1,74 mld | **−0,85 mld** |

Il risultato delle aziende peggiora (da −1,28 a −2,59 mld) e il consolidato
passa da +0,89 a −0,85. Nel 2024 le peggiori: ULSS 3 Serenissima −150,7 mln,
Policlinico Umberto I −144,2, San Camillo −135,0, Azienda integrata di Verona
−106,7, ASL Città di Torino −97,4.

## Verifiche fatte sulla fonte

1. **Consolidato = dataset regionale**: ricavi e risultato coincidono con
   `bdap_ssn_conto_economico` **su 13/13 anni, scarto 0,0 mln**.
2. **Chiave** `(anno, bdap, ssn, voce)` **unica** (76.124 righe, 0 duplicati nel 2024).
3. **Schema stabile** in tutti i 13 anni.
4. **Codici**: `sezione` solo A/B/C/D/E/Y/Z; `prospetto` non applicabile qui.

## Caveat

- **`000` presente in 15 regioni su 21** nel 2024: in sei regioni l'ente regione
  non ha righe nel CE per-ente.
- **Entità ambigue**: un codice BDAP può avere più codici SSN (INRCA: 916/920/921),
  la chiave include entrambi.
- **Entità cessate**: da 254 (2012) a 217 (2024).
- **Trimestri esclusi**: i package trimestrali (56) hanno lo stesso schema ma il
  periodo sta nel titolo, non in una colonna.

Vedi `notes.md` per le scelte tecniche e i prossimi passi.
