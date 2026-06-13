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

24 colonne. Ogni riga è un ricorso depositato al Consiglio di Stato in materia di appalti pubblici, con dati ANAC integrati (CIG, importi gara, stazione appaltante, settore, provincia).

**Copertura**: 2023–2026 (4 anni), aggiornamento mensile.

## Perché vale la pena

- **Tema civico**: il contenzioso sugli appalti pubblici è un indicatore di salute del sistema degli acquisti pubblici
- **Già integrato**: la fonte unisce dati GA + ANAC (CIG, importi)
- **Granularità**: ogni ricorso è un record, con dati economici e geografici
- **Collegabile**: via CIG ad altri dataset ANAC

## Output minimo atteso

- `mart_ricorsi_sede_classificazione`: conteggio e importi per anno/sede/classificazione
- `mart_ricorsi_territorio_settore`: conteggio e importi per provincia/anno/settore

## Criterio di promozione

- Run completo su tutti gli anni (2023-2026) con validazioni green
- Mart popolati con dati coerenti anno su anno
- Note sui limiti del dataset documentate

## Stato

- intake
- **2026-06-13**: issue #496 aperta, branch creato, run completo verde

## Prossimo passo

- review e merge PR
