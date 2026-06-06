# Terna capacita rinnovabile per territorio

## Domanda

Dove si concentra la capacita rinnovabile installata in Italia e quali territori risultano piu attrezzati, a fine anno, per fonte e nel confronto 2015-2024?

## Dataset

- Fonte: Terna, download center ufficiale sulla capacita installata delle fonti rinnovabili
- Formato: XLSX, sheet `Export`
- Livello disponibile in raw: provincia
- Perimetro intake: serie storica 2015-2024 (dicembre di ogni anno)

## Perche vale la pena testarlo

- fonte ufficiale forte e tema civico leggibile
- filone complementare al candidate Terna gia esistente sulla generazione
- primo taglio territoriale semplice senza forzare join o letture causali

## Output minimo atteso

- candidate DI riproducibile per 2015-2024
- clean provinciale coerente con il tracciato Terna
- mart v0 su capacita netta aggregata per regione e fonte
- notebook v0 di sanity check sul mart

## Criterio di promozione

- raw, clean e mart rigenerabili per 10 annualita (2015-2024)
- documentazione coerente con il perimetro reale
- notebook v0 eseguibile senza trasformarlo in analisi pubblica

## QC — 2026-05-01

| Layer | 2023 | 2024 | Status |
|---|---|---|---|
| raw | 1161 | 1071 | SUCCESS |
| clean | 1160 | 1070 | ✅ |
| mart | 100 | 100 | ✅ |

**Colonne raw → clean (6/6):** `Anno→anno`, `Tipo capacità→tipo_capacita`, `Regione→regione`, `Provincia→provincia`, `Fonti→fonti`, `Potenza efficiente (MW)→potenza_mw`

**Note:**
- 1 riga filtrata in clean (entrambi gli anni): footer `Applied filters...` senza anno numerico
- `potenza_mw` null in clean: atteso — Terna riporta null per combinazioni regione/fonte senza capacita installata (non zero implicito)
- I null propagano al `SUM` in mart: 21 null in mart 2023, 2 in mart 2024
- **Lorda = Netta**: delta 0.0000% su entrambi gli anni — stesso pattern di `terna-electricity-by-source`

## Stato

- **runnable**

## Prossimo passo

- PR post-merge: push clean → GCS/BQ, aggiorna registry
