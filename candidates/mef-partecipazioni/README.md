# MEF Partecipazioni Pubbliche

## Domanda guida

Quali amministrazioni locali dichiarano più partecipazioni, e il profilo delle partecipate per tipo e territorio conferma l'intuizione attesa oppure no?

## Fonte

- **MEF** — Dipartimento dell'Economia
- URL: https://www.de.mef.gov.it/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni/
- Formato: CSV, `;`, latin-1
- Licenza: da verificare (fonte pubblica MEF)

## Perimetro

- **Anni disponibili**: 2020, 2021, 2022, 2023 (tutti con URL dedicato sul portale MEF)
- Granularità: partecipazione dichiarata (una riga = una relazione amministrazione-partecipata)
- Chiavi territoriali: regione, provincia, comune per amministrazione e per partecipata
- Copertura: tutte le PA obbligate alla dichiarazione (comuni, regioni, ministeri, enti pubblici)

## Struttura

- **84 colonne** comuni a tutti gli anni — perimetro stabile cross-year
- **9 colonne anno-specifiche** (Fatturato N, Risultato d'esercizio N, Partecipata bilancio N approvato) — variano per ogni anno e sono state escluse per garantire schema costante
- Una riga = una partecipazione (relazione many-to-one amministrazione → partecipata)

## Schema variability

| Anno | Colonne totali | Colonne escluse (anno-specifiche) |
|---|---|---|
| 2020 | 93 | 9 |
| 2021 | 93 | 9 |
| 2022 | 93 | 9 |
| 2023 | 93 | 9 |

Le colonne excluse contengono l'anno nel nome (es. `Fatturato 2023`) e cambiano per ogni anno di rilevazione. La clean.sql usa solo le 84 colonne comuni per garantire schema costante nel tempo.

## Rischi noti

- **Copertura**: chi non ha dichiarato non compare; file di adempimento come riferimento per stimare il gap
- **Serie storica**: 2020-2023, schema stabile su 84 colonne comuni
- **Encoding**: latin-1 con caratteri non standard residui
