# elezioni-comunali

Risultati delle elezioni comunali in Italia per comune, candidato e lista (2016-2024).

**Fonte**: Eligendo — Archivio storico elettorale del DAIT (Ministero dell'Interno)
**Licenza**: dati pubblici

## Domanda guida

Come si distribuisce il voto alle elezioni comunali nei comuni italiani? Quali candidati e liste vincono?

## Dataset

- **Copertura**: 2016–2024 (7 tornate, anni con elezioni)
- **Granularità**: comunale per candidato, lista e turno
- **Righe**: ~43.000
- **Colonne**: 15 (data_elezione, regione, provincia, comune, turno, candidato, lista, voti_candidato, voti_lista, ...)
- **Comuni coperti**: 623–3.653 per anno (dipende da scadenze mandato)

## Stato

`candidate` — run verificato su 7 anni.

## Gap noti
- 2022 e 2023 non inclusi (formato XLSX non ancora gestito dal preprocess.py)
