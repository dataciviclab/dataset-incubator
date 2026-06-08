# Notes: istat_pil_territoriale

## Domanda guida
Support dataset per normalizzazione PIL e Valore Aggiunto territoriale.

## Rischi noti

1. **Edizioni multiple**: SDMX contiene edizioni (2025M1, 2025M6, 2025M12) con valori leggermente diversi per lo stesso anno. Clean.sql prende l'ultima edizione.
2. **Timeout SDMX**: ISTAT SDMX è talvolta lento (radar YELLOW). Timeout sporadici possibili.
3. **Break di serie**: I conti economici hanno cambi di metodologia (SEC2010, cambio anno base). I dati concatenati (L_2020) attenuano il problema. Per ora usiamo solo prezzi correnti (V).
4. **Province storiche**: Alcune province sono cambiate nel periodo (es. Monza Brianza creata nel 2009). I dati SDMX riflettono la geografia corrente.
5. **Extra-Regio (ITZ)**: Include attività non attribuibili territorialmente (sedi diplomatiche, piattaforme offshore). Va gestito separatamente se serve PIL regionale puro.

## Perimetro v0

- Anni: 2000-2024
- Livello: regioni + province (107)
- Metrica: PIL prezzi correnti (B1GQ_B_W2_S1, V)
- Filtro: solo ADJUSTMENT='N' (grezzi)

## Trigger per estensione

- Aggiungere Valore Aggiunto per branca ATECO
- Aggiungere PIL concatenato (L_2020) per serie reali
- Espandere a dati trimestrali (se disponibili)
