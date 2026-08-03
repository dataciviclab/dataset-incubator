# Notes — membri-governo

## Fonte

- Endpoint SPARQL: `https://dati.camera.it/sparql` (Virtuoso)
- Graph: default (le query su GRAPH esplicito con OPTIONAL danno risultati falsi — lezione da camera-votazioni)
- Licenza: CC BY 3.0

## Query produzione

- `GROUP BY ?membro` + `MAX(...)` per ogni campo (fix duplicati da OPTIONAL multipli — pattern consolidato)
- Una sola query: 7.579 righe < soglia WAF 10k → nessuna paginazione
- `accept_format: sparql-results+json` (con "csv" l'endpoint restituisce Turtle — lezione da camera-deputati)

## Volumi (verificati 2026-08-03)

- Membri governo: **7.579** (match esatto issue #786)
- Copre dal Regno d'Italia (regno_19, 1862) alla Repubblica (repubblica_06+)

## URI e persona_id

- Membri: `membroGoverno.rdf/mg5660_6_25` (Repubblica) vs `mgr19_16_21` (Regno, con 'r')
- Persona: `persona.rdf/p5660` (Repubblica) vs `persona.rdf/pr20` (Regno, con 'r')
- `persona_id`: id numerico dall'URI (regexp con pattern dedicato per `pr`) —
  **stessa normalizzazione di camera_deputati_legislature** → join per persona_id

## Regno vs Repubblica

- Membri del Regno (URI `mgr...`): `ruolo` e `start_date` NON valorizzati —
  la data è solo nella label ("dal 21.06.1894 al 01.12.1894")
- Decisione: ruolo/start_date NULL per il Regno (parsing label opzionale futuro)
- La colonna `ruolo` usa `ocd:membroGoverno` (predicato, non il tipo) — verificato

## Gender

- Il grafo governo NON espone foaf:gender sulla persona → non incluso
- Il gender si ottiene con join a `camera_deputati_legislature` per persona_id

## Join

- `persona_id` → join con `camera_deputati_legislature` (deputati) e futuro senato/governo
- `governo` → URI ocd/governo.rdf/g25 (anagrafica governi non estratta)
- `organo` → URI ocd/organoGoverno.rdf/og25_1 (dicastero)

## 2026-08-03 — infrastruttura Camera degradata (500/502/503)

Le pagine .rdf individuali (es. .../membroGoverno.rdf/mg302351_...) danno 500
con errore interno: "Connection to http://dati.camera.it refused" — la
dereferenziazione usa un path interno http:// (non https) rotto. L'endpoint
SPARQL alterna 200/502/503 (già documentato). NON impatta la pipeline (usiamo
l'endpoint, non la dereferenziazione) — i raw scaricati restano validi.
