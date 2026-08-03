# Notes — camera-incarichi

## Fonte

- Endpoint SPARQL: `https://dati.camera.it/sparql` (Virtuoso)
- Graph: default (le query su GRAPH esplicito con OPTIONAL danno risultati falsi — lezione da camera-votazioni)
- Licenza: CC BY 3.0

## Query produzione

La query usa `GROUP BY ?incarico` + `MAX(...)` per ogni campo: il pattern senza GROUP BY
produce righe duplicate (prodotto cartesiano tra i OPTIONAL — verificato: ogni incarico
appariva 2 volte). Stesso fix di `camera_votazioni_sparql`.

## Volumi (verificati 2026-08-03)

- Incarichi: **3.096** (match esatto con issue #787)
- Gruppi parlamentari distinti: **215**
- Max incarichi per legislatura: 510 (repubblica_17) → **1 pagina basta, sotto WAF 10k**

## Date

- `start_date`/`end_date`: formato YYYYMMDD (stringa) dal sorgente → normalizzate a DATE nel clean
- `end_date` può essere assente (incarico in corso) → NULL

## Legislatura

- URI: `http://dati.camera.it/ocd/legislatura.rdf/repubblica_17` → clean estrae `repubblica_17`
- Copre Regno + Costituente + Repubblica (il join con deputati richiede la stessa normalizzazione)

## Join

- `deputato`: URI ocd/deputato.rdf/d306020_17 → join con `camera_deputati_legislature.deputato`
- `gruppo`: URI ocd/gruppoParlamentare.rdf/gr1612 → (anagrafica gruppi non ancora estratta)

## Limiti

- Copre solo gli incarichi nei **gruppi parlamentari**; commissioni/uffici parlamentari
  (graph `ocd/ufficiParlamentari/`) non ancora estratti — da verificare in estensione futura
- Il `owl:sameAs` (Wikidata/DBpedia) citato nell'intake non risulta nel graph default:
  0 risultati verificati → non incluso
