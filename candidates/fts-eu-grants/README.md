# FTS EU Grants — Finanziamenti UE erogati in Italia

**Fonte**: [Financial Transparency System (FTS)](https://commission.europa.eu/funding-tenders/financial-transparency-system_en) — registro ufficiale dei beneficiari di fondi UE.

**Dataset**: `fts_eu_grants`

## Domanda guida

Chi riceve finanziamenti UE in Italia? Quanto, per quali programmi, e con quali modalità?

## Contenuto

Tutti i beneficiari di fondi UE con sede in Italia, dal 2020 a oggi. Per ogni grant:

- Beneficiario (nome, città, tipo: università, impresa, ONG, PA...)
- Programma (Horizon Europe, Erasmus+, Digital Europe, LIFE, CERV...)
- Importo contrattato, consumato e stimato
- Dipartimento UE responsabile
- Date progetto

## Perimetro iniziale

- Tutti i grant UE erogati a beneficiari italiani
- Anni: 2020–2024
- ~5.000-7.000 grant/anno

## Fonti collegate

- **TED contract_notices** — bandi di gara UE in Italia
- **OpenCoesione** — fondi strutturali in Italia
- **RNA aiuti_stato** — aiuti di Stato alle imprese

## Perché vale la pena

I grant UE diretti all'Italia sono 17 miliardi di EUR in 5 anni (2020-2024, escluso RRF). Sapere quali programmi, quali beneficiari e dove finiscono i soldi europei è una domanda di trasparenza diretta — risponde alla discussion #395 (13 domande verificate).

## Output minimo atteso

- `mart_trend_anno`: contrattato/consumato per anno + RRF separato (17,05 mld no-RRF, assorbimento 72%)
- `mart_sintesi_programma`: per programma-anno (Horizon 4,75 mld, CEF Transport 1,11 mld)
- `mart_sintesi_beneficiario`: per tipo beneficiario (Private Companies 56%)
- `mart_top_beneficiari`: top beneficiari per importo (CNR, Polimi, Leonardo, BBT)

## Criterio di promozione

Promuovere quando: (1) i numeri del trend e delle classifiche sono verificati e citabili; (2) la discrepanza vs discussion #395 è riconciliata; (3) almeno una risposta della discussion è chiusa con dati.

## Stato / prossimo passo

- **Stato**: candidate a standard v1 (2026-08-03) — 4 mart serie, script fixato (schema variabile), run passed 5 anni, readiness 8/8
- **Prossimo passo**: merge PR; post-merge: catalog aggiornamento; riconciliazione numeri con discussion #395 (data-researcher)
