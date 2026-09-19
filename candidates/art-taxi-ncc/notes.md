## Tecnico

- CSV diretto, delim `;`, UTF-8, header. Nessuna conversione necessaria.
- Granularità: comune. 176 righe, `comune` univoco (primary_key verificata).
- `NCC` ha NULL su alcuni comuni (es. Carbonia, Procida): dato mancante, non zero — lasciato NULL.
- Toolkit 1.51.0: `dataset.tags`/`category` richiesti dal gate strict (1.44.0 li rifiuta).

## Analitico

- Top taxi/10k: Taormina (39,3), Milano (35,5), Procida (31,9), Roma (28,0) — mix di mete turistiche e grandi città, plausibile.
- Mart `mart_taxi_ncc_per_capite`: ratio con `NULLIF` su popolazione zero.

## Cautele

- Snapshot 2024 singolo — nessuna serie storica (FOIA #15 su data-advocacy per 2019-2024).
- Solo comuni con licenze (~176): assenza ≠ zero, è fuori perimetro fonte.
- `regione` non presente nel file — confronto Nord/Sud richiede join ISTAT comuni.
