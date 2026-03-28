# Terna capacita rinnovabile per territorio

## Domanda

Dove si concentra la capacita rinnovabile installata in Italia e quali territori risultano piu attrezzati, a fine anno, per fonte e nel confronto minimo 2023-2024?

## Dataset

- Fonte: Terna, download center ufficiale sulla capacita installata delle fonti rinnovabili
- Formato: XLSX, sheet `Export`
- Livello disponibile in raw: provincia
- Perimetro intake: dicembre 2023 e dicembre 2024

## Perche vale la pena testarlo

- fonte ufficiale forte e tema civico leggibile
- filone complementare al candidate Terna gia esistente sulla generazione
- primo taglio territoriale semplice senza forzare join o letture causali

## Output minimo atteso

- candidate DI riproducibile per 2023-2024
- clean provinciale coerente con il tracciato Terna
- mart v0 su capacita netta aggregata per regione e fonte
- notebook v0 di sanity check sul mart

## Criterio di promozione

- raw, clean e mart rigenerabili per entrambi gli anni
- documentazione coerente con il perimetro reale
- notebook v0 eseguibile senza trasformarlo in analisi pubblica

## Stato

- intake

## Prossimo passo

- verificare il run completo 2023-2024 e lasciare il candidate pronto per review DI
