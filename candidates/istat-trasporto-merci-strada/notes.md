# Notes — istat-trasporto-merci-strada

## Tecnico

- Fonte: ISTAT `121_330` via **DBnomics** (`type: dbnomics`, provider ISTAT).
- Copertura 2008-2024; `years: [2026]` è l'anno di output.
- Clean: `anno`, `regione_carico`, `regione_scarico`, `merce_nst`, `tipo_trasporto`, `unita`, `classe_distanza`, `valore`.
- Mart `mart_merci_per_direttrice`: filtra `unita = 'GC_TKM'`, tiene le righe con entrambe le regioni `IT%`, esclude `IT -> IT` e calcola uscita/entrata per regione.

## Analitico

- Le coppie **regione → regione non esistono**: i flussi sono `regione -> Italia` (uscita) e `Italia -> regione` (entrata). Il mart **non è una matrice origine-destinazione**, misura quanto ogni regione spedisce e riceve rispetto al resto d'Italia.
- `quota_pct` è la quota della regione sul totale dei flussi regionali (esclusi `IT -> IT`).

## Cautele

- Non leggere il mart come una matrice OD: manca il dettaglio regione → regione.
- Non aggregare `unita` diverse da `GC_TKM`: misurano grandezze non confrontabili.
- `tipo_trasporto`, `merce_nst` e `classe_distanza` hanno subtotali (`ALL`, `TOTAL`): il mart filtra i subtotali; leggendo il clean, filtrare prima di sommare.
- Confronto con il ferroviario solo a parità di unità (`GC_TKM`) e per anno.
