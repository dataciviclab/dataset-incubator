# notes.md — bdap-ssn-ce-per-ente

## Source-check (2026-11-09)

Famiglia OpenBDAP: *"Modello di rilevazione del Conto Economico degli enti del
SSN"* (livello per ente, package **annuale**) — 13 package, 2012-2024,
~76.000 righe/anno.

| verifica | esito |
|---|---|
| 13 UUID raggiungibili | ✅ 200 su tutti |
| schema | ✅ 10 colonne, `;`, `cp1252`, coda vuota |
| chiave `(anno, bdap, ssn, voce)` | ✅ unica (0 duplicati nel 2024) |
| consolidato (`999`) = dataset regionale | ✅ ricavi e risultato, scarto 0,0 mln su 13/13 anni |
| quadratura del risultato | ✅ `000` + enti ≈ `999` (2024: 1,739 − 2,586 = −0,847 vs −0,851) |
| additività di ricavi/costi | ❌ **non additivi**: compensazioni interne (~20 mld nel 2024) |
| `000` presente | ⚠️ 15 regioni su 21 nel 2024 |

## Scelte di mapping

1. **`tipo_riga` esplicito**, come nel dataset per-ente dello Stato Patrimoniale:
   `ente` (si somma), `regione` (`000`, soggetto reale), `consolidato` (`999`,
   totale). Convenzione **invertita** rispetto al modello LEA.

2. **Ricavi e costi non si sommano.** Le aziende si scambiano prestazioni
   (mobilità) e ricevono trasferimenti dalla regione: il consolidato elimina
   quei flussi. Nel 2024: enti 170,3 mld di ricavi vs consolidato 150,1. Il
   risultato invece quadra. Il README lo dice in testa, perché è l'errore più
   facile da fare con questo dataset.

3. **Solo package annuali.** La famiglia ha 69 item: 13 annuali + 56 trimestrali
   ("2024/I Trim."). I trimestrali hanno lo stesso schema ma il periodo sta nel
   **titolo del package**, non in una colonna: `url_suffix_by_year` mappa un solo
   UUID per anno, quindi servirebbero 4 raw source (Q1..Q4) con `trimestre`
   iniettato. Rimandato a un dataset dedicato.

4. **Totali di sezione affidabili.** A differenza dello Stato Patrimoniale, qui
   `AZ9999`/`BZ9999`/`ZZ9999` ci sono per tutte le righe (sono la base del mart
   regionale già in produzione): nessuna derivazione necessaria.

5. **Regex dei livelli in cifre arabe** (`A.1`, `A.1.A`, `B.10`), come il CE
   regionale — non quella romana dello Stato Patrimoniale.

## Ponte verso SIOPE (verificato)

`Codice Ente BDAP` (18 cifre) ≠ `codice_ente` SIOPE (15 cifre), ma il **codice
fiscale** unisce:

```
Codice Ente BDAP → bdap_anagrafe_enti.Id_Ente → CF → SIOPE anagrafica.cf
```

Verificato su questo stesso file: **149/149 enti del 2024** con CF e match
SIOPE. Con questo dataset il ponte diventa operativo: costo per ente (qui) vs
cassa per ente (SIOPE).

## Cosa resta aperto

- **Trimestri**: 56 package, 4 raw source con `trimestre` iniettato, 2012-2025.
  Aggiungono tempestività (il 2025 è già disponibile a trimestri).
- **`000` mancante in 6 regioni** (2024): se serve il conto dell'ente regione
  per tutte, va verificato sulla fonte.
- **Consolidamento**: se serve un mart "sistema sanitario regionale", va usata
  la riga `999`; se serve "aziende", la riga `ente`. Mescolarle senza
  `tipo_riga` è l'errore da evitare.
