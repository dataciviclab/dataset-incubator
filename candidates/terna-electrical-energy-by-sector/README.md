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
Nota: 2015-2020 dati disaggregati (più righe per provincia/settore), 2021-2024 già aggregati. Il SUM nel mart normalizza — i totali sono comparabili tra tutti gli anni.
