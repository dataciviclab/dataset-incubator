# mef-irpef-regionale

**Domanda:** Come varia la distribuzione del reddito tra le regioni italiane nel periodo 2017–2025, e quali sono le aree a maggiore vulnerabilità economica?

**Fonte:** MEF Dipartimento Finanze — Open Data IRPEF regionale
URL: `https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?opendata=yes`

**Perimetro:** Regioni italiane × classi di reddito complessivo × anno
- Anni: 2017–2025 (9 anni di dati — pre-2017 non disponibili sul portale MEF)
- Classi: 34 fasce (da "minore di -1.000" a "oltre 300.000")
- Righe: 714 per anno (21 regioni × 34 classi di reddito)

**Qualificatore:** `usable-with-enrichment` — servono mapping regione→macro-area e classi→fascia per l'analisi di disuguaglianza.

**Note:** Questo candidate è dedicato all'IRPEF regionale. NON va confuso con `irpef-comunale` che ha granularità comunale (~7900 comuni) e periodi parziali (2019-2023).
