# Camera Deputati — Legislature

## Domanda

Quanti deputati hanno fatto parte di ciascuna legislature della Camera?

## Fonte

[dati.camera.it/sparql](https://dati.camera.it/sparql) — endpoint SPARQL del Catalogo linked-data Camera dei deputati.

## Perimetro

Tutti i deputati di tutte le legislature della Repubblica Italiana (fino alla XIX). Ogni deputato può comparire in più legislature — la chiave è `(deputato, legislature)`.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|---|
| `deputato` | string | URI RDF del deputato |
| `cognome` | string | Cognome (da `foaf:surname` o `rdfs:label` per deputati storici) |
| `nome` | string | Nome (da `foaf:firstName` o `rdfs:label` per deputati storici) |
| `legislatura` | string | Codice legislature (es. "costituente", "regno_01", ..., "repubblica_19") |
| `gender` | string | Sesso (`male`/`female`/`null`) |

## Output

- **Raw**: CSV da SPARQL, paginazione automatica (3 pagine × 10k)
- **Clean**: 27.618 righe, 5 colonne, **99% nomi popolati**
- **Mart**: `mart_deputati.parquet` — un record per `(deputato, legislature)`

## Note tecniche

- I deputati della Repubblica hanno `foaf:surname` + `foaf:firstName`; quelli del Regno hanno solo `rdfs:label` nel formato "NOME COGNOME, Legislatura...". Il clean.sql unifica le due fonti.
- Il WAF della Camera blocca risposte >10k righe — risolto con `pages: 3, step: 10000` nel dataset.yml
- 9 righe su 27.618 (0.03%) non hanno nome — deputati con mandato senza dati anagrafici completi nel sistema
- Gender: popolato solo per deputati recenti (Repubblica) — storico ha `null`

## Run

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/camera-deputati-legislature/dataset.yml --years 2024
```

## Perché vale la pena

Chi sono i deputati e cosa hanno fatto in Parlamento: anagrafica completa (biografia, foto, mandato) + join con gli incarichi nei gruppi parlamentari (support `camera-incarichi`). La chiave `persona_id` collega Camera, Senato e Governo — base per analisi trasversali (issue #787).

## Output minimo atteso

- `mart_legislatura_genere`: composizione Camera per legislatura e genere
- `mart_top_mandati`: persone con più legislature (carriere lunghe)
- Join con `camera-incarichi` per (persona_id, legislatura)

## Criterio di promozione

Promuovere quando: (1) i numeri di composizione per legislatura sono verificati; (2) il join con gli incarichi è stabile; (3) una domanda civica usa i dati (es. presenza femminile per legislatura).

## Stato / prossimo passo

- **Stato**: candidate esteso a standard v1 (2026-08-03) — 10 colonne, mart serie, readiness 8/8
- **Prossimo passo**: merge PR; post-merge catalog; esplorare composizione gruppi per legislatura
