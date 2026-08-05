# Notes — camera-gruppi

## Fonte

- Endpoint SPARQL: `https://dati.camera.it/sparql` (Virtuoso Camera)
- Classe: `ocd:gruppoParlamentare` — graph default (come membri-governo)
- Licenza: CC BY 3.0

## Query produzione

```sparql
SELECT ?gruppo (MAX(?label) AS ?label) (MAX(?legislatura) AS ?legislatura)
WHERE {
  ?gruppo a ocd:gruppoParlamentare .
  OPTIONAL { ?gruppo rdfs:label ?label . }
  OPTIONAL { ?gruppo ocd:rif_leg ?legislatura . }
}
GROUP BY ?gruppo
```

GROUP BY + MAX (pattern standard anti-duplicati OPTIONAL). 239 righe < soglia WAF 10k → una sola query.

## Volumi (verificati 2026-08-04)

- **239 gruppi** (tutte le legislature, dalla Costituente alla XIX)
- La maggior parte ha `label` (es. "MOVIMENTO 5 STELLE (M5S) (19.03.2013...") e `rif_leg`
- Alcuni URI sono fusioni (es. `gr433+434`) senza label — gruppi confluenti, tenuti con nome NULL

## Label

- Formato: `NOME (ACRONIMO) (gg.mm.aaaa-gg.mm.aaaa)` — contiene le date di esistenza del gruppo
- La label non viene parsata (le date restano nel testo); se servono date strutturate, lavoro futuro

## Legislatura

- URI `ocd/legislatura.rdf/repubblica_17` → clean estrae `repubblica_17`
- Stessa normalizzazione di `membri_governo` e `camera_incarichi` → join coerente

## Join

- `gruppo`: URI `ocd/gruppoParlamentare.rdf/gr1612` → join con `camera_incarichi.gruppo`

## Limiti

- I gruppi "Misto" esistono in ogni legislatura con URI diversi (gr207, gr279...) — corretto, sono entità distinte
- URI concatenati (gr433+434) senza label: non risolvibili singolarmente dalla fonte
