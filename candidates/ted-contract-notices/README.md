# TED Contract Notices — Bandi di gara UE in Italia

**Fonte**: [TED (Tenders Electronic Daily)](https://ted.europa.eu/) — versione europea dell'albo degli appalti pubblici.

**Dataset**: `ted_contract_notices`

## Domanda guida

Quali sono i bandi di gara pubblici europei in Italia? Chi bandisce, per cosa, con quali importi e procedure?

## Contenuto

Tutti i bandi di gara pubblicati su TED da stazioni appaltanti italiane (o con sede in Italia), dal 2012 a oggi. Per ogni bando:

- Stazione appaltante (nome, città, tipo, attività principale)
- Oggetto del contratto (CPV, tipo contratto: servizi/lavori/forniture)
- Valore stimato in euro
- Procedura (aperta, ristretta, negoziata, ecc.)
- Criterio di aggiudicazione (prezzo più basso vs OEPV)
- Localizzazione NUTS (regione/provincia)
- Flag fondi UE, accordo quadro, opzioni, rinnovo
- Date (pubblicazione, scadenza offerte, durata)

## Perimetro iniziale

- Solo **Contract Notices** (bandi di gara, non aggiudicazioni)
- Filtrato per **Italia** (ISO_COUNTRY_CODE = 'IT')
- Anni: 2012–2023
- ~48.000 bandi/anno

## Output minimo atteso

- Clean parquet con schema normalizzato
- Mart analitico con flag soprasoglia UE, fasce di valore, macroarea NUTS1
- Joinabilità con ANAC (via CPV, NUTS, stazione appaltante)

## Fonti collegate

- **ANAC bandi_gara** — appalti nazionali italiani (sotto e sopra soglia)
- **ANAC CIG** — dettaglio lotti e aggiudicazioni
- **RNA aiuti_stato** — aiuti di Stato alle imprese
