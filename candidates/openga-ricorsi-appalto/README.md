# openga-ricorsi-appalto

Ricorsi pervenuti in materia d'appalto al Consiglio di Stato, integrati con dati ANAC.

**Fonte**: OpenGA (Giustizia Amministrativa) — `https://openga.giustizia-amministrativa.it`
**Dataset ID**: `cds-ricorsi-pervenuti-in-materia-d-appalto`
**Protocollo**: CKAN
**Frequenza**: mensile
**Licenza**: CC-BY 4.0

## Domanda

Quali sono i volumi e la distribuzione del contenzioso sugli appalti pubblici in Italia? Quali settori, territori e stazioni appaltanti sono più coinvolti?

## Dataset

24 colonne. Granularità: ricorso × lotto/CIG (un ricorso può riguardare più lotti). La chiave del ricorso è `numero_ricorso`. Dati ANAC integrati (CIG, importi gara, stazione appaltante, settore, provincia).

**Copertura**: 2023–2026 (4 anni), aggiornamento mensile.

## Perché vale la pena

- **Tema civico**: il contenzioso sugli appalti pubblici è un indicatore di salute del sistema degli acquisti pubblici
- **Già integrato**: la fonte unisce dati GA + ANAC (CIG, importi)
- **Granularità**: record-level con chiave ricorso e dati economici/geografici
- **Collegabile**: via CIG ad altri dataset ANAC

## Output minimo atteso

- `mart_ricorsi_sede_classificazione`: ricorsi e gare per anno/sede/classificazione
- `mart_ricorsi_territorio_settore`: ricorsi e gare per provincia/anno/settore

## Criterio di promozione

- Run completo su tutti gli anni (2023-2026) con validazioni green
- Mart popolati con dati coerenti anno su anno
- Note sui limiti del dataset documentate

## Stato

- intake
- **2026-06-13**: issue #496 aperta, branch creato, run completo verde

## Prossimo passo

- review e merge PR
