# sbarchi-migranti-italia

Arrivi giornalieri di migranti via mare in Italia (2019-2026).

**Fonte**: [ondata/liberiamoli-tutti](https://github.com/ondata/liberiamoli-tutti/tree/main/sbarchi-migranti/dati) — dati estratti da PDF del Ministero dell'Interno.
**Licenza**: CC-BY 4.0 (onData)

## Domanda guida

Quante persone arrivano via mare in Italia ogni giorno? Come evolve il fenomeno anno per anno?

## Dataset

- **Copertura**: settembre 2019 – maggio 2026
- **Granularità**: giornaliera (una riga per giorno)
- **Righe**: 2.465 (giorni)
- **Arrivi totali (serie giornaliera)**: ~502.600
- **Colonne**: 4 (data, valore, note, fonte)

### Nota sul dato

Il file sorgente è una **concatenazione di report** (colonna `Data_Report`): ogni report riporta i giorni del suo mese fino alla sua data, quindi lo stesso giorno compare più volte e il valore viene rivisto nei consolidamenti. Il `clean` tiene **una riga per giorno** (l'ultimo report), altrimenti le somme gonfiano di ~1,5×.

Limite: la serie **giornaliera** si ferma al report di fine mese, quindi non recepisce i consolidamenti successivi (che invece onData pubblica in `sbarchi-mensili.csv`) e dal **giugno 2026** il PDF non riporta più il dettaglio giornaliero (si ferma al 31 maggio 2026). I totali annui da questa serie sono quindi leggermente inferiori a quelli ufficiali (es. 2023: 155.515 vs 157.651).

## Stato

`candidate` — run verificato su snapshot 2026 (file unico multi-anno).
