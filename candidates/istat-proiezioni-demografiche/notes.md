# Note tecniche — istat-proiezioni-demografiche

## Canale

- ZIP statico: `https://demo.istat.it/data/previsioni/Previsioni-Popolazione_per_eta-Regioni.zip`
- 22 CSV regionali, 18.816 righe ciascuno (56 anni × 3 sessi × 112 età)
- Precedentemente: SDMX (flaky) → RPC SPA (complesso) → ZIP (pulito)

## Struttura ZIP

Ogni CSV: 3 righe di intestazione, poi header `Anno;Sesso;Età;...;Scenario mediano;...`
- Sesso: Maschi / Femmine / Totale
- Età: 0–110+ / Totale
- Scenario mediano + IC 50/80/90%

## Italia

Il ZIP non ha Italia totale — `mart_italia` calcola la somma delle 22 regioni.

## Intake

Creato 2026-10-14. Richiesto per progetto interno (welfare/pensioni).
