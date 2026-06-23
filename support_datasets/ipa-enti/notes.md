# ipa-enti — note tecniche

## CSV parsing

Il dump DataStore IPA ha 35 colonne (incluse `_id` e 4 social URL).
Alcuni campi numerici (Codice_natura, Codice_ateco) sono spesso vuoti,
causando auto-deduction errata in DuckDB strict mode.

**Fix**: tutte le colonne sono lette come VARCHAR esplicitamente nel
`clean.read.columns`. Il clean.sql applica CAST a VARCHAR + trim per
normalizzare.

## Colonne rimosse

- `_id`: chiave interna DataStore, non serve
- `Url_facebook`, `Url_linkedin`, `Url_twitter`, `Url_youtube`:
  social media, non rilevanti per anagrafica advocacy

## Validazione

- clean: min_rows=10000 (attesi ~23700)
- mart: pass-through, min_rows=10000

## Cross-reference con data-advocacy

Il mapping tra source_id DA e denominazione IPA non è diretto.
Va costruita una lookup table separata (da fare).
