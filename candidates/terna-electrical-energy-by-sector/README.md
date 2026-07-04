# terna-electrical-energy-by-sector

Consumi elettrici per settore economico e provincia (GWh).

## Domanda guida

Quanta elettricità consumano le famiglie, l'industria, i servizi e l'agricoltura in Italia? Come si distribuisce il consumo per provincia?

## Fonte

TERNA S.p.A. — Download Center
<https://dati.terna.it/download-center>

## Shape

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno` | INTEGER | Anno di riferimento |
| `regione` | VARCHAR | Regione |
| `provincia` | VARCHAR | Provincia |
| `settore` | VARCHAR | Domestico, Industria, Servizi, Agricoltura |
| `consumo_gwh` | DOUBLE | Consumo in GWh |

## MART

`mart_consumi_settore_provincia`: consumi per anno, provincia e settore.

Nota: gli anni 2015-2020 hanno dati disaggregati (fino a 106k righe/anno) mentre 2021-2024 sono pre-aggregati (428 righe/anno). Il SUM nel mart normalizza — i totali sono comparabili tra tutti gli anni (es. Bergamo/Industria: 4.771 GWh nel 2015 vs 4.886 GWh nel 2024).

## Setup

L'ambiente necessita `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` per lo script di fetch che rimuove il footer "Applied filters" dal XLSX di TERNA. Vedere `notes.md` per dettagli tecnici.
