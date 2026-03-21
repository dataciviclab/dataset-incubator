# Source-check Template

Usa questo template quando vuoi verificare rapidamente una fonte pubblica prima
di aprire una Discussion `Datasets` o una issue di intake.

Compilalo in modo leggero: l'obiettivo non è scrivere una nota perfetta, ma
capire se la fonte regge davvero.

---

# [Fonte o dataset]

## Fonte

- ente o fonte ufficiale:
- pagina sorgente:
- link diretto al file o endpoint:
- formato: `csv` / `xlsx` / `zip` / `json` / altro

## Accesso reale

- il file o endpoint risponde davvero?
- ci sono redirect?
- serve JavaScript o login?
- `content-type` coerente?

## Cosa contiene

- granularità:
- copertura temporale:
- una riga rappresenta cosa?
- chiave territoriale presente?
- file unico o uno per anno?
- colonne o campi principali:

## Perché può essere rilevante

Scrivi in 2-4 righe perché questa fonte può valere un intake.

Punta a una domanda concreta, non a una descrizione generica del dataset.

## Rischi o limiti

- accesso opaco?
- licenza poco chiara?
- formato sporco?
- chiavi territoriali deboli?
- output minimo che non regge senza join?
- serie troppo corta?

## Verdict

Scegli uno:

- `go Discussion`
- `support dataset`
- `watchlist`
- `scartare`
- opzionale: `pronto per intake diretto`

## Prossimo passo

Indica un solo next step pratico:

- aprire una Discussion `Datasets`
- aprire una issue di intake
- tenere in watchlist con trigger di riapertura
- scartare
