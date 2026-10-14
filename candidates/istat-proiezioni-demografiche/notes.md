# Note tecniche — istat-proiezioni-demografiche

## Canale (2026-10-14)

- **demo.istat.it** (`RPCCerca.php`) — SPA API JSON, POST form-encoded
- SDMX ISTAT (`165_889` / `DCIS_PREVDEM1`) è flaky da ore — non usato
- `preprocess.py` fetch: Italia + ripartizioni + 21 regioni × 6 componenti × 56 anni
- ~168 chiamate RPC, rate-limit 0.3s → ~2 min

## API demo.istat.it

```
POST https://demo.istat.it/app/RPCCerca.php
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest

componenti=1&annoda=2025&annoa=2080&ripartizione=26&regione=
&hid-i=PPR&hid-a=2025&hid-l=it&hid-cat=PPR
&hid-dati=dati-form-1&hid-tavola=tavola-form-1&btnricerca-1=Cerca
```

Risposta: JSON con `datatable.data[]` — colonne: `denominazione`, `anno`, `inf90/80/50`, `median`, `sup50/80/90`.

Form-1 `componenti`: 1=popolazione, 2=nati, 3=morti, 8=saldo_naturale, 9=saldo_migr_estero, 10=saldo_migr_interno.

Codici ripartizione: 26=Italia, 23=Nord, 27=Nord-ovest, 28=Nord-est, 24=Centro, 25=Mezzogiorno.

Codici regione (RRPC.php): 1-22 (mappa in preprocess.py).

## Copertura

- anni: 2025–2080 (orizzonte lungo)
- scenario: mediano (median)
- territori: 27 (Italia + ripartizioni + regioni)
- componenti: 6

## SDMX alternativa

`165_889` (`DCIS_PREVDEM1`) — se SDMX torna, si può aggiungere come seconda source o sostituire il preprocess.

## Intake

Creato da sessione Lab 2026-10-14. Richiesto per progetto interno (welfare/pensioni).
