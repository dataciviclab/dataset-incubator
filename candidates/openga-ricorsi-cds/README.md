# openga-ricorsi-cds — Ricorsi Pendenti Consiglio di Stato

**Fonte**: [OpenGA - Giustizia Amministrativa](https://openga.giustizia-amministrativa.it/dataset/cds-ricorsi-pendenti-per-periodo)

## Dataset

Ricorsi pendenti presso il Consiglio di Stato, aggregati per sede e mese.
Ogni riga rappresenta il numero di ricorsi pendenti in un dato mese per una sede del CdS.

**Periodo**: 2023-2026 (aggiornamento continuo)
**Ultimo anno**: 2026 parziale (fino a marzo)

**Colonne**:
- `anno` — anno di riferimento
- `mese` — mese (1-12)
- `codice_sede` — codice numerico della sede
- `nome_sede` — denominazione della sede (es. CONSIGLIO DI STATO)
- `numero_ricorsi_pendenti` — ricorsi pendenti a fine mese

## Domanda civica

*Quanto cresce il backlog di ricorsi pendenti al Consiglio di Stato? Il carico di lavoro è stabile o in aumento?*

**Nota**: il dataset contiene lo *stock* mensile di ricorsi pendenti (fotografia a fine mese), non i flussi di deposito/decisione. Per misure di durata o velocità servono i dataset sui flussi (cds-ricorsi-pervenuti, cds-ricorsi-definiti).

## Perché vale la pena

- Join con `civile_flussi` (già pubblicato) per confrontare volumi di pendenti tra giustizia ordinaria e amministrativa
- Serie mensile (2023-oggi) per analisi trend del carico di lavoro
- Copertura: tutte le sedi del Consiglio di Stato

## Output minimo atteso

- Dataset clean con ricorsi pendenti per mese e sede
- Mart annuale con indicatori aggregati

## Criterio di promozione

- Run OK su tutti gli anni
- Verifica join con `civile_flussi`
- Notebook v0 con trend dei ricorsi pendenti

## Stato

- candidate: run completato RAW→CLEAN→MART su 2023-2026 (tutti passati ✅)
- readiness: ready (5/5 checks)
- notebook v0 verificato
- issue: #379


