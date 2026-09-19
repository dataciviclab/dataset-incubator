# opencoesione-soggetti

Soggetti coinvolti nei progetti di politiche di coesione in Italia (2007-2027).

## Fonte

OpenCoesione / PCM — Dipartimento Politiche di Coesione. Dati harvestati su dati.gov.it.
File Parquet scaricabile da opencoesione.gov.it. Licenza CC BY 4.0.

## Cosa contiene

Soggetti (enti, imprese, amministrazioni) coinvolti nei progetti di coesione come beneficiari, partner, coordinatori. Ogni riga collega un soggetto (CF) a un progetto (COD_LOCALE_PROGETTO) con ruolo, forma giuridica e sede.

## Output

- `clean`: 22 colonne selezionate, filtrate per CF e progetto non nulli
- `mart_beneficiari`: aggregato per CF con conteggio progetti e distinzione beneficiari

## Uso

```bash
toolkit run --config candidates/opencoesione-soggetti/dataset.yml
```
