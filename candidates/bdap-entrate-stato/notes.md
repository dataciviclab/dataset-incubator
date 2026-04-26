# Notes — bdap-entrate-stato

## Tech

- fonte: MEF BDAP — Rendiconto Pubblicato, Serie Storica Entrate per Titolo/Natura/Tipologia/Provento
- URL: `https://bdap-opendata.rgs.mef.gov.it/export/csv/Rendiconto-Pubblicato---Serie-storica---Entrate-Aggregato-per-Titolo-Natura-Tipologia-e-Provento.csv`
- formato: CSV `;`-delimitato, encoding `cp1252`
- serie storica: **2008–2024** (17 anni) in un unico file cumulativo
- raw row count: **1320** righe — tutte le righe hanno codice_titolo, codice_natura, codice_tipologia non null
- clean row count: **1320** righe (raw-faithful — nessun filtro sostanziale, solo `is not null` su esercizio)
- mart row count: **104** righe (aggregato per anno + titolo + natura)

## Struttura clean

11 colonne (raw-faithful, nessuna logica interpretativa):

| colonna | tipo | nota |
|---|---|---|
| esercizio_finanziario | int | anno contabile |
| codice_titolo / titolo | string | classificazione principale |
| codice_natura / natura | string | sottoclasse |
| codice_tipologia / tipologia | string | dettaglio |
| codice_provento / provento | string | voci specifiche |
| previsioni_definitive_cp/cs | double | previsioni competenza/cassa |

**Nota sui filtri**: il vecchio clean.sql aveva filtri `codice_titolo is not null` ecc. nella WHERE — questi non filtravano nulla sui dati attuali (tutti i codici erano già presenti), ma erano concettualmente sbagliati: se il raw avesse dati mancanti, verrebbero rimossi in clean invece che in mart. Il clean corretto è raw-faithful: solo `is not null` su esercizio per rimuovere righe non parsing.

## Struttura mart

`mart_entrate_titolo_natura_anno` — 104 righe:
- GROUP BY esercizio_finanziario, codice_titolo, titolo, codice_natura, natura
- somma previsioni CP e CS
- quota percentuale sul totale anno (quota_cp, quota_cs)
- `titolo_breve`: TITOLO I - ... → I (strip prefix con regexp)

## Caveat analitici

- `Previsioni Definitive` ≠ incasso effettivo
- confronto anni richiede attenzione sulla stabilità delle classificazioni contabili
- riguarda lo Stato centrale, non il perimetro consolidato PA

## Stato

- run SUCCESS: `20260426T110853Z_e5861e7b`
- clean raw-faithful: 1320 righe
- mart: 104 righe (2008–2024)