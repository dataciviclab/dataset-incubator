# notes.md — bdap-ssn-stato-patrimoniale

## Source-check (2026-11-08)

Famiglia OpenBDAP: *"Modello di rilevazione dello Stato Patrimoniale degli enti
del SSN a livello Regionale"* — 13 package, 2012-2024, ~0,9 MB per anno.

| verifica | esito |
|---|---|
| schema stabile 2012-2024 | ✅ stesse 7 colonne, `;`, `cp1252`, coda vuota |
| chiave (anno, regione, voce) | ✅ unica su tutte le 13 annualità |
| attivo = passivo (derivati dalle sezioni) | ✅ dal 2020 scarto 0 su 21/21; Sardegna 2024 +34,2 mln |
| utile d'esercizio ↔ CE `ZZ9999` | ✅ 0 su 2020, 2022-2024; Sardegna 2012-2015 da revisione; Calabria 2021 assente nel CE |
| copertura territoriale | ✅ 21 territori in tutti gli anni |

## Scelte di mapping

1. **Totali derivati, non letti.** La riga `AZZ999` (D. Totale attivo) manca in 9
   regioni nel 2024, 11 nel 2020 e in tutte nel 2012. Lo stesso vale per `PZZ999`.
   Il mart somma i totali di sezione (`AAZ999`, `ABZ999`, `ACZ999` per l'attivo;
   `PAZ999`..`PEZ999` per il passivo), che invece ci sono quasi sempre (21/21 per
   l'attivo, 20/21 per il passivo — a Trento manca `PEZ999`, che vale zero).

2. **Conti d'ordine fuori dai totali.** `ADZ999` e `PFZ999` sono voci di memo
   (garanzie e impegni): sommarle gonfierebbe l'attivo senza che ci sia un bene.

3. **Codice a 6 caratteri.** Posizione 1 = prospetto (`A`/`P`), posizione 2 =
   sezione, posizione 3 = `Z` per i totali di sezione. Il clean espone `prospetto`,
   `sezione`, `riga_sintesi`; `livello` e `voce_livello1` vengono dalla descrizione
   (`A.I.1.a)`), come nel Conto Economico.

4. **`riga_sintesi` invece di `is_totale`.** Il validator del toolkit segnala i
   nomi che suggeriscono un numero accanto a un booleano; stesso nome usato nel
   candidate del Conto Economico, per coerenza.

## Ponte verso il livello per-ente (verificato)

La famiglia per-ente esiste (`modello di rilevazione dello stato patrimoniale
degli enti del ssn`, 13 item, ~6,8 MB; e `conto economico degli enti del ssn`, 69
item con trimestri). La chiave per collegarla a SIOPE **non** è il codice:

- BDAP `Codice Ente BDAP`: 18 cifre (es. `729242930477377001`)
- SIOPE `codice_ente`: 15 cifre (es. `024073904000000`)

Il ponte verificato è il **codice fiscale**:

```
CE per-ente.Codice Ente BDAP == bdap_anagrafe_enti.Id_Ente
        → anagrafe.CF
        → SIOPE anagrafica enti.CF → codice_ente SIOPE
```

Testato sui 149 enti del CE 2024: **149/149 con CF, 149/149 con match SIOPE**
(tipo ente `ASL`). Quindi il livello per-ente è collegabile ai dati di cassa
SIOPE per singola azienda.

## Cosa resta aperto

- **SP per-ente** (13 item, 6,8 MB, ~36k righe/anno): stessa struttura, grana per
  azienda. Da prendere dopo questo, con la stessa chiave CF.
- **CE per-ente**: 76k righe/anno, 149 aziende, trimestri nel titolo del package.
  Richiede di fissare la semantica `000`/`999`, che qui è **invertita** rispetto
  al modello LEA (`000` = ente regione, `999` = consolidato).
- **2012-2015**: scarti di quadratura fino a 222 mln e piccole divergenze con il
  CE. Sono anni con edizioni della fonte riviste: se servono, vanno documentati
  per singola regione e anno.
