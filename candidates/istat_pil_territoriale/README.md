# istat_pil_territoriale — PIL regionale e provinciale

**Support dataset** — ISTAT SDMX Dataflow 93_498 (DCCN_PILT)

## Fonte

ISTAT — Conti economici territoriali (PIL lato offerta)
SDMX-CSV: `https://esploradati.istat.it/SDMXWS/rest/data/93_498_DF_DCCN_PILT_1/all?format=csv`

## Copertura

- **Territoriale**: nazionale, macro-aree, **21 regioni**, **108 province**
- **Temporale**: 1995 → 2023 (regionale/provinciale), 1995 → 2024 (nazionale)
- **Metriche**: 
  - PIL ai prezzi di mercato (`B1GQ_B_W2_S1`)
  - Valore Aggiunto (`B1G_B_W2_S1`)
  - Imposte nette sui prodotti (`D21X31_C_W2_S1`)
- **Valutazione**: prezzi correnti (V), concatenati (L_2020), anno precedente (Y)
- **Frequenza**: annuale
- **Unità**: milioni di euro

## Uso previsto

Support dataset per normalizzare e contestualizzare analisi esistenti:
- Incidenza spesa pubblica su PIL (Consip, BDAP, pensioni)
- PIL pro-capite per confronti territoriali (join con popolazione_istat_comunale)
- Contesto macroeconomico per analisi sanitarie, fiscali, ambientali

## Join keys

- `territorio_codice` → codici ISTAT/NUTS
- `anno` → anno di riferimento

## Output

- **clean** (10.167 righe): territorio_codice, livello, tipo_dato_codice, valutazione_codice, anno, valore_mln_eu
- **mart** (3.128 righe): pivoted per territorio/anno con pil_mln_eu, va_mln_eu, imposte_nette_mln_eu

## Run

✅ Config valida. Run 2024: raw✅ clean✅ mart✅ (passato).
