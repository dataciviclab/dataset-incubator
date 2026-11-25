# notes.md — bdap-ssn-sp-per-ente

## Source-check (2026-11-09)

Famiglia OpenBDAP: *"Modello di rilevazione dello Stato Patrimoniale degli enti
del SSN"* (livello per ente, senza suffisso "a livello regionale") — 13 package,
2012-2024, ~6,8 MB per anno, ~36.000 righe.

| verifica | esito |
|---|---|
| 13 UUID raggiungibili | ✅ 200 su tutti |
| schema | ✅ 10 colonne, `;`, `cp1252`, coda vuota |
| chiave `(anno, bdap, ssn, voce)` | ✅ unica (0 duplicati nel 2024) |
| consolidato (`999`) = dataset regionale | ✅ scarto 0,0 mln su 13/13 anni |
| quadratura per ente | ✅ 210/217 enti a 0 nel 2024 (max residuo 4 €); +34,2 mln sulla riga `consolidato` della Sardegna |
| `AZZ999` disponibile | ⚠️ 140 enti su 217 (totale derivato dalle sezioni) |

## Scelte di mapping

1. **Tre tipi di riga espliciti.** `tipo_riga` distingue `ente` (aziende da
   sommare), `regione` (`000`, ente regione — soggetto reale) e `consolidato`
   (`999`, totale regionale). Nel modello LEA gli stessi codici hanno significato
   **opposto**: là `000` è l'aggregato e `999` l'ente regione. Non è una
   convenzione stabile tra file, va verificata ogni volta.

2. **Chiave a quattro colonne.** Un codice BDAP può avere più codici SSN: l'INRCA
   compare tre volte (916, 920, 921) con denominazioni diverse — sono unità
   contabili distinte (presidi) i cui importi si sommano. La chiave del clean è
   `(anno, codice_ente_bdap, codice_ente_ssn, codice_voce)`; senza il codice SSN
   si perdono 1.196 righe nel solo 2024 (14.079 su 13 anni).

3. **Totali derivati.** Come nel dataset regionale, `AZZ999`/`PZZ999` non sono
   affidabili (mancano per 77 enti su 217 nel 2024): attivo e passivo si sommano
   dalle sezioni `AAZ999`+`ABZ999`+`ACZ999` e `PAZ999`..`PEZ999`.

4. **Regex dei livelli in cifre romane.** Il prospetto usa `A.I)`, `A.I.1.a)`,
   `B.II.7.e.1)`: stesso pattern del dataset regionale, non quello del Conto
   Economico (cifre arabe). `livello` = numero di punti, `voce_livello1` = prime
   due componenti.

## Ponte verso SIOPE (verificato sul CE per-ente)

Il codice ente BDAP (18 cifre) e il codice ente SIOPE (15 cifre) sono sistemi
diversi. Il ponte è il **codice fiscale**:

```
Codice Ente BDAP → bdap_anagrafe_enti.Id_Ente → CF → SIOPE anagrafica.cf
```

Verificato sui 149 enti del Conto Economico per-ente 2024: **149/149 con CF,
149/149 con match SIOPE**. Lo stesso passaggio vale per questo dataset, che usa
la stessa anagrafica.

## Cosa resta aperto

- **Conto Economico per-ente** (69 item, trimestri nel titolo del package):
  complemento naturale, con la stessa chiave CF. Lì va fissata anche la
  dimensione trimestrale, che nel titolo non è una colonna.
- **`000` mancante in 4 regioni** (2024): se serve il bilancio dell'ente regione
  per tutte, va verificato sulla fonte (probabilmente non pubblicato).
- **Entità cessate**: il numero di enti scende da 252 (2012) a 217 (2024). Chi
  costruisce serie storiche per ente deve gestire i codici che spariscono.
