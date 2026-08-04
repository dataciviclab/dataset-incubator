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
       (MAX(?data) AS ?data) (MAX(?natura) AS ?natura) (MAX(?fase) AS ?fase)
WHERE { GRAPH <http://dati.senato.it/ddl/19> {
  ?ddl osr:idDdl ?idDdl .
  OPTIONAL { ?ddl osr:titolo ?titolo . } OPTIONAL { ?ddl osr:statoDdl ?stato . }
  OPTIONAL { ?ddl osr:dataPresentazione ?data . }
  OPTIONAL { ?ddl osr:natura ?natura . } OPTIONAL { ?ddl osr:fase ?fase . }
} }
GROUP BY ?ddl
```

## Fase — codice atto

`fase` è il codice dell'atto (es. C.1774 = atto Camera, S.782 = atto Senato),
5.114 valori unici. I blank node (`nodeID://b307199465`) sono esclusi nel clean
(`CASE WHEN fase LIKE 'nodeID://%' THEN NULL ELSE fase END`).

## Struttura reale: una riga = una versione dell'atto nell'iter

Verificato 2026-08-04 (review): un ddl ha PIÙ righe — una per versione dell'atto
nel suo iter tra i rami. Es. ddl 54667:
- S.1670 (Senato) → S.1670-B (appr. definit. Legge)
- C.2473 (Camera) → C.2473-B (approvato)

Quindi `fase` = numero atto per ramo (non codice fase univoco), e la sequenza
delle righe col `progressivo_iter` ricostruisce l'iter completo (ping-pong
Camera↔Senato). 5.124 righe = 4.671 ddl × versioni. PK: (id_ddl, fase).

Nota: `numero_legge`/`data_legge` solo per i ddl approvati (727, 14%) —
data_legge può essere 2100-01-01 (placeholder Senato per legge pubblicata).

## Colonne disponibili (25 predicati, verificate)

La fonte espone 25 predicati sui ddl — estraiamo i 13 con valore per la domanda:
id_ddl, ddl_url, titolo, stato, data_presentazione, natura, fase, ramo,
iniziativa, progressivo_iter, legislatura, numero_legge, data_legge.

## Estensione futura

- Legislature 13-19: graph `ddl/13`..`ddl/19` (pattern `{year}` → `{leg}`)
- `senatore`/`rif_deputato`: presentatori → join con anagrafica persone (persona_id)
- `assegnazione`/`tipoCommissione`/`dataAssegnazione`: iter per commissione

## 2026-08-04 — 27 colonne complete, 3 sorgenti (limite WAF)

Il WAF Senato rifiuta query SPARQL > ~15 colonne (403 su 1.642 char, ok su 1.498).
La query completa (25 predicati) è spezzata in 3 sorgenti (q1: 11 col, q2a: 8,
q2b: 7), unite con read.mode: all + union_by_name. Il clean ricombina con
GROUP BY ddl + MAX (pattern identico alla query SPARQL).

Copertura verificata: 15/27 colonne al 100% (titolo, stato, data, natura, fase,
ramo, iniziativa, iter, legislatura...); numero_legge/data_legge 14% (solo
approvati — corretto); relatore 38%; testo_approvato 7.8%; testo_unificato e
stralcio ~0% (rari nella fonte). Nessun dato troncato: tutte le colonne della
fonte sono esposte.

Lezione: prima di ogni candidate SPARQL, confrontare predicati disponibili vs
colonne estratte (gate standard). Il mode all unisce per union_by_name (concat)
→ serve GROUP BY + MAX nel clean per ricombinare sorgenti complementari.

## 2026-08-04 — mart_iter_tempi (valorizzazione domanda #781)

Aggiunta la mart che risponde alla domanda guida ("come nasce e muore una legge"):
- 345 ddl diventati legge con data_legge reale (escluso placeholder 2100-01-01)
- media 295 giorni dall'iter, min 30, max 1.372 (3,7 anni)
- per ddl: n_versioni (ping-pong tra rami), ramo, giorni/mesi iter
- aggregata per id_ddl (il clean ha una riga per versione dell'atto)
- NOTA: il placeholder 2100-01-01 del Senato (legge pubblicata senza data nota)
  è escluso dalla mart — 1 solo ddl nel dataset, non distorce i tempi
