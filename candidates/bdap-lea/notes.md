# notes.md — bdap-lea

## Stato (2026-11-09)

Candidate rivisto: esteso da 2019-2024 a **2012-2024**, aggiunti i flag che
rendono il dataset sommabile, aggiunto un mart dei totali.

## Cosa non andava

1. **Il totale pubblicato veniva buttato.** Il clean filtrava le 5 voci di
   totale (`19999`, `29999`, `39999`, `48888`, `49999`) per evitare il double
   counting, ma sono le **uniche** sommabili: le voci di dettaglio sono
   gerarchiche (genitore + figli) e sommarle gonfia il totale di ~2,4 volte.
   Verificato su ASL TO3 2024: 2,77 mld di dettaglio contro 1,17 mld di totale.

2. **La serie sembrava rotta nel 2019.** Sommando il dettaglio: 204,8 mld (2018)
   → 330,1 mld (2019), un salto del 61%. In realtà è un artefatto: nel 2019 il
   modello cambia la gerarchia: le voci di dettaglio distinte scendono da **117
   a 104** (121 → 109 contando anche i totali). Usando il totale pubblicato la
   serie è continua: 141,9 (2018) → 146,2 (2019) → 174,2 (2024).

3. **`000` e `999` erano descritti al contrario.** Il README diceva «000 =
   aggregati regionali, 999 = enti regione». Verificato: `000` = **ente regione**
   (soggetto reale: Abruzzo 44,1 mln con la voce `49999` nel 2024), `999` =
   **consolidato regionale** (3,32 mld con `49999`). Sommare tutte le righe
   invece dà 148 mln e 13,96 mld: sono i numeri gonfiati dalla gerarchia, non
   la grandezza dell'ente. Il comportamento del dataset era comunque corretto
   perché escludeva entrambi; ora è esplicito con `tipo_riga`.

## Scelte di mapping

- **`tipo_voce`** (`totale`/`dettaglio`): unica difesa contro la gerarchia.
- **`tipo_riga`** (`ente`/`regione`/`consolidato`): stessa semantica dei dataset
  CE/SP per-ente.
- **`mart_spesa_enti` invariato nel perimetro**: filtra `tipo_voce='dettaglio'`
  e `tipo_riga='ente'`. I conteggi per anno sono identici a prima (2019: 16.126,
  2024: 20.036), quindi nessun consumer esistente cambia.
- **`mart_totale_ente`**: nuovo, ente × anno, con il totale pubblicato e la
  composizione. `quadratura` = 0,00 su 13/13 anni (identità `49999 = 19999 +
  29999 + 39999 + 48888`).
- **Macro standard** (`cast_int`, `cast_double`, `normalize_string`) al posto di
  `try_cast`.
- **`primary_key`** `(anno, bdap, ssn, voce)` dichiarata: unica; senza il codice
  SSN si perdono 1.702 righe nel 2024.

## Schema drift

`Oneri Finanziari` esiste solo in 2019, 2021, 2022, 2024; assente in 2012-2018,
2020 e 2023. Gestito con `align_by_header` (colonne assenti → NULL).

Nel 2019 cambia anche il numero di voci: il dettaglio passa da **117 a 104**
voci distinte (121 → 109 includendo i totali). Il dettaglio non è confrontabile
tra il prima e il dopo, i totali sì.

## Cosa resta aperto

- **2025**: non ancora nel catalogo OpenBDAP (la famiglia si ferma al 2024).
- **Confronto con il CE per-ente**: qui il totale enti 2024 è 174,2 mld, il CE
  per-ente dice 170,3 mld di ricavi. La differenza (~4 mld) va spiegata: perimetri
  e competenza possono diverge, ma non è stato verificato ente per ente.
- **Regione `000`**: il mart dei totali è solo per ente; se serve il totale
  dell'ente regione, basta filtrare `tipo_riga='regione'` nel clean.
