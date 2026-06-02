# ISTAT Nonprofit — Censimento permanente delle Istituzioni non profit

Risorse umane (istituzioni, dipendenti, volontari) delle istituzioni non profit in Italia,
per provincia, regione, settore di attività e forma giuridica.

## Domanda civica

Quante istituzioni non profit sono attive in Italia, in quali settori operano,
quanti dipendenti e volontari impiegano, e come si distribuiscono per provincia e regione?

## Fonte

- **Ente**: ISTAT — Tavole del Censimento permanente delle Istituzioni non profit
- **URL**: https://www.istat.it/statistiche-per-temi/censimenti/istituzioni-non-profit/
- **File**: `Tavole_nonprofit_2023.xlsx`
- **Formato**: XLSX (22 tavole)
- **Periodicità**: annuale (Registro statistico), aggiornamento ottobre 2025
- **Granularità**: provinciale, regionale, nazionale

## Dati verificati (2023)

| Metrica | Valore |
|---|---|
| Istituzioni non profit | 368.367 |
| Dipendenti | 949.200 |
| Province coperte | 107 (tutte) |
| Prima provincia per istituzioni | Roma (26.253) |
| Prima provincia per dipendenti | Roma (113.610) |

## Perimetro v0

- **Fonte**: Sheet 22 (Tavola 22 — Istituzioni non profit e dipendenti per provincia)
- **Anno**: 2023
- **Output**: `mart_nonprofit_province` — codice provincia, provincia, istituzioni, dipendenti

## Prossimi sviluppi v1

- Sheet 1: istituzioni e dipendenti per forma giuridica e regione
- Sheet 2: istituzioni e dipendenti per settore di attività e regione
- Serie storica: scaricare anni precedenti (2016-2022) dal Registro statistico
- SDMX come fonte complementare per risorse umane
