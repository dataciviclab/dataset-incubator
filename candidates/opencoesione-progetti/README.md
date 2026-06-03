# opencoesione-progetti

Progetti finanziati dalle politiche di coesione in Italia (2007-2027).

## Fonte

OpenCoesione / PCM — Dipartimento Politiche di Coesione. Dati harvestati su dati.gov.it.
File Parquet scaricabile da opencoesione.gov.it. Licenza CC BY 4.0.

## Cosa contiene

2.3 milioni di progetti con 95 colonne: dati anagrafici, finanziari (finanziamenti, impegni, pagamenti), tematici e di avanzamento.

## Output

- `clean`: 25 colonne selezionate (da 95), filtrate per macroarea e tema non nulli
- `mart_macroarea_tema`: aggregato per ciclo × macroarea × tema con ratio spesa e impegni

## Uso

```bash
toolkit run full --config candidates/opencoesione-progetti/dataset.yml
```
