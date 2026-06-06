# Notes — bdap-spese-stato

## Tech

- fonte: MEF BDAP — Rendiconto Pubblicato, Serie Storica Spese per Amministrazione/Missione/Programma/Macroaggregato
- URL: `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/7f30045d-c95e-44ec-83b8-f39f60e7256a.csv`
- formato: CSV `;`-delimitato, encoding `cp1252` (ISO-8859-1)
- serie storica: **2008–2024** (17 anni) in un unico file cumulativo
- raw row count: **11.881** righe
- colonna 13 sempre vuota → esclusa dal clean (solo column00–column11 mappate)
- BDAP server è lento (~60s per risposta) — timeout HTTP alto necessario

## Struttura clean

12 colonne (raw-faithful, nessuna logica interpretativa):

| colonna | tipo | nota |
|---|---|---|
| esercizio_finanziario | int | anno contabile |
| stato_previsione | string | codice ministero |
| amministrazione | string | es. "MINISTERO DELL'ECONOMIA" |
| missione | string | 37 missioni |
| programma | string | programma di spesa |
| udv_livello_1/2/3 | string | unità di voto gerarchica |
| codice_puntato_udv | string | codice aggregato |
| macroaggregato | string | categoria economica |
| previsioni_definitive_cp/cs | double | previsioni competenza/cassa |

## Struttura mart

`mart_spese_missione_anno` — aggregato per anno × missione:
- GROUP BY esercizio_finanziario, missione
- somma previsioni CP e CS
- quota percentuale sul totale anno (quota_cp, quota_cs)

## Relazione con bdap_entrate_stato

- **Gemello funzionale**: stessa fonte, stesso periodo (2008-2024), stesso atto (Rendiconto Pubblicato)
- Le entrate sono classificate per Titolo/Natura/Tipologia/Provento
- Le spese per Amministrazione/Missione/Programma/Macroaggregato
- Non joinabile direttamente: le chiavi contabili sono diverse, richiederebbe un mapping tabellare

## Caveat analitici

- `Previsioni Definitive` ≠ spesa effettiva
- confronto anni richiede attenzione sulla stabilità delle classificazioni (missioni/programmi)
- riguarda lo Stato centrale, non il perimetro consolidato PA
- 111 valori null su Previsioni CP (da verificare dopo il run)

## Stato

- intake #437
- in bootstrap
