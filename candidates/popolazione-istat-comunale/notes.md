# Note per il dataset Popolazione ISTAT Comunale

## Scopo

Fornire una panoramica dei dati demografici a livello di comune per gli anni 2019‑2025.

## Fonte dei dati

ISTAT – Istituto Nazionale di Statistica, dataset ufficiale.

## Come eseguire le query

Il file `sql/clean.sql` contiene la query di pulizia. È possibile eseguire:

```bash
python -m dataset_incubator.run_query \\
  --dataset popolazione-istat-comunale \\
  --sql sql/clean.sql
```

## Metriche disponibili

- `popolazione_totale`
- `maschi`
- `femmine`

## Contatti

Per segnalare problemi aprire una issue nella repository.