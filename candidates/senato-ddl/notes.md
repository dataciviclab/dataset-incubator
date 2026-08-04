# Notes — senato-ddl

## Fonte

- Endpoint SPARQL: `https://dati.senato.it/sparql`
- **GET obbligatorio**: il POST dà 403 (a differenza della Camera che accetta entrambi). Il plugin SPARQL fa POST→GET fallback → funziona ma con retry.
- Namespace: **`http://dati.senato.it/osr/`** (NON ocd: come la Camera)
- Graph: `http://dati.senato.it/ddl/{legislatura}` — XIX = `ddl/19` (issue #781, perimetro iniziale)
- Licenza: CC BY 3.0

## ⚠️ WAF Senato — query costose rifiutate (403)

Verificato 2026-08-03: il WAF rifiuta con 403 le query con:
- `CONTAINS` nel FILTER **combinato** con GROUP BY
- COUNT DISTINCT globali pesanti (su più pattern)

Soluzione: query produzione SENZA CONTAINS (GROUP BY + MAX solo), il filtro `/ddl/` si fa **nel clean** (`WHERE ddl LIKE '%/ddl/%'`).

## DDL vs iterDdl — la distinzione chiave

L'endpoint espone ogni ddl in DUE forme:
- `/ddl/58074`: ha i **metadati** (titolo, stato, dataPresentazione) ← teniamo questi
- `/iterDdl/51155`: solo l'iter (fase), metadati vuoti ← esclusi

**9.775 ddl totali** (con idDdl), ~50% in ciascuna forma → ~4.900 ddl con metadati completi.

## Volumi (verificati 2026-08-03)

- Soggetti graph ddl/19: 1.130.984 (la maggior parte sono componenti: articoli, commi)
- DDL con idDdl: **9.775**
- DDL con URI /ddl/ (metadati): ~4.900

## Query produzione

```sparql
SELECT ?ddl (MAX(?idDdl) AS ?idDdl) (MAX(?titolo) AS ?titolo) (MAX(?stato) AS ?stato)
       (MAX(?data) AS ?data) (MAX(?tipo) AS ?tipo) (MAX(?fase) AS ?fase)
WHERE { GRAPH <http://dati.senato.it/ddl/19> {
  ?ddl osr:idDdl ?idDdl .
  OPTIONAL { ?ddl osr:titolo ?titolo . } OPTIONAL { ?ddl osr:statoDdl ?stato . }
  OPTIONAL { ?ddl osr:dataPresentazione ?data . }
  OPTIONAL { ?ddl osr:tipoIniziativa ?tipo . } OPTIONAL { ?ddl osr:fase ?fase . }
} }
GROUP BY ?ddl
```

## Fase — blank node

`fase` può essere un blank node (`nodeID://b307199465`) — esclusi nel clean
(`CASE WHEN fase LIKE 'http://%' THEN fase ELSE NULL END`).

## Estensione futura

- Legislature 13-19: graph `ddl/13`..`ddl/19` (pattern `{year}` → `{leg}`)
- `senatore`/`rif_deputato`: presentatori → join con anagrafica persone (persona_id)
- `assegnazione`/`tipoCommissione`/`dataAssegnazione`: iter per commissione
