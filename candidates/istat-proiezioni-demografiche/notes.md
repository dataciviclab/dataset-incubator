# Note tecniche — istat-proiezioni-demografiche

## Canale

- `type: sdmx` · agency `IT1` · flow `165_889` (`DCIS_PREVDEM1`) v1.0
- endpoint: esploradati.istat.it (default toolkit post-fix #444)
- **SDMX ISTAT è flaky**: timeout/redirect frequenti. Il config ha `retries: 3` e `timeout: 180`.

## Fonti alternative se SDMX fallisce

1. **demo.istat.it** (`?i=PPR`): SPA, download manuale dal browser
2. **IstatData**: stesso dataflow, download manuale CSV
3. Comunicato stampa ISTAT 2026: prospetti riassuntivi

## Dopo il primo run

- Verificare le colonne raw (DSD): `SEX`, `AGE`, eventuali `SCENARIO` / `CI_LEVEL`
- Adattare il filtro scenario nel clean (default: tutto, poi restringere a mediano)
- `AGE`: se classi quinquennali, il `primary_key` del clean è corretto; se totale, adattare

## Copertura attesa

- anni: 2025–2080 (orizzonte lungo)
- territori: IT + 20 regioni NUTS2
- sesso: maschi / femmine
- età: classi (da verificare dopo primo run)

## Intake

Creato da sessione Lab 2026-10-14. Richiesto per progetto interno (welfare/pensioni).
