# EU Call Open — Call UE aperte e in arrivo

**Fonte**: [EU Funding & Tenders Portal](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home) via SEDIA Search API (backend pubblico del portale).

**Dataset**: `eu_call_open`

## Domanda guida

Quali call di finanziamento UE sono aperte o in arrivo, con quale scadenza e budget?

## Contenuto

Topic/call del portale F&T con status **Open for submission** o **Forthcoming**, periodo di programmazione 2021-2027:

- Identificativo topic e call (es. `ERC-2027-STG`)
- Titolo, stato, programma (Horizon Europe, Digital Europe, LIFE, CERV, ...)
- Data apertura, **deadline**, modello (single/multi-stage)
- Budget aggregato dal campo `budgetOverview`
- URL della pagina topic sul portale

## Perimetro iniziale

- Solo **grant topics** (type=1), non tenders EuropeAid
- Status: open + forthcoming (closed = archivio enorme, da valutare a parte)
- Lingua risultati: EN
- Snapshot ~1k topic, ~400 con deadline futura

## Perché vale la pena

Il Lab copre i fondi UE già erogati (`fts_eu_grants`) e la coesione (`open-coesione`), ma non le **call aperte a cui candidarsi**. Questo dataset colma quel gap ed è la base per una futura catena call → progetto → rendicontazione (vedi `call_id` in FTS).

## Output atteso

- `mart_scadenze`: call con deadline futura ordinate per imminenza
- `mart_per_programma`: n call e budget per programma UE

## Limiti

- API non ufficiale-stabile (frontend EC, nessun versioning) — vedi notes.md
- Status "Open" non basta: parte degli open ha deadline passata → filtrare `ha_scadenza_futura`
- Budget a livello aggregato (budgetOverview), non contrattuale
- Non c'è filtro Italia sensato sui topic (EU-wide)

## Stato / prossimo passo

- **Stato**: candidate v0 — open + forthcoming, 2 mart
- **Prossimo passo**: run toolkit, review, eventuale estensione (closed, join FTS)
