# opencoesione-soggetti — note

## Fonte

- **Ente**: PCM — Dipartimento Politiche di Coesione / OpenCoesione
- **Portale di riferimento**: dati.gov.it (organization: pcm-opencoesione)
- **File**: `soggetti_20260430.parquet` (~6M righe)
- **Licenza**: CC BY 4.0
- **Aggiornamento**: 2026-04-30 (data dump)

## Collegamento con progetti

Ogni soggetto è collegato a un progetto tramite `COD_LOCALE_PROGETTO`. Per trovare i beneficiari di un progetto, joinare con `opencoesione_progetti` sul campo `COD_LOCALE_PROGETTO`.

## Uso nel terzo settore

Il dataset è usato da `terzo-settore-intelligence` per identificare quali ETS hanno partecipato a progetti di fondi coesione, tramite join su `OC_CODICE_FISCALE_SOGG`.

## Output v0

Tabella `mart_beneficiari`:
- `codice_fiscale`, `denominazione`, `forma_giuridica`, `comune_sede`
- `attivita_ateco`, `dimensione`
- `n_progetti` (totale), `n_progetti_beneficiario` (solo come beneficiario)
