# Notes — senato-anagrafica

## Fonte

- Endpoint SPARQL Senato: `https://dati.senato.it/sparql` (GET obbligatorio, POST 403 → fix toolkit v1.47.3+)
- Namespace `osr:` (`http://dati.senato.it/osr/`), graph `http://dati.senato.it/composizione/19`
- Licenza: CC BY 3.0

## Query produzione

```sparql
SELECT ?senatore (MAX(?label) AS ?label)
       (MAX(?dataNascita) AS ?dataNascita) (MAX(?citta) AS ?citta)
WHERE {
  GRAPH <http://dati.senato.it/composizione/19> {
    ?senatore a osr:Senatore .
    OPTIONAL { ?senatore rdfs:label ?label . }
    OPTIONAL { ?senatore bio:birth ?b . ?b bio:date ?dataNascita . }
    OPTIONAL { ?senatore bio:birth ?b2 . ?b2 bio:place ?pl . ?pl rdfs:label ?citta . }
  }
}
GROUP BY ?senatore
```

GROUP BY + MAX (pattern standard). 212 righe < soglia WAF 10k → una sola query, nessuna paginazione.

## Struttura della fonte (verificata 2026-08-04)

- `senatore`: URI `http://dati.senato.it/senatore/N` — id locale Senato (NON coincide con persona_id Camera)
- `rdfs:label`: nome completo ("Gianluca Cantalamessa", "Luca De Carlo")
- `bio:date`: data di nascita ISO (1968-02-02)
- `bio:place` → nodeID → `osr:Citta` con `rdfs:label` = città ("Napoli", "Pieve Di Cadore")
- Copertura verificata sul parquet (2026-08-04): **212/212 con data e luogo di nascita (100%)**

## Perimetro

- **XIX legislatura** (graph composizione/19) — coerente con `senato-ddl`/`senato-firmatari`
- Estensione a legislature 13-19 (graph `composizione/13`..`/19`): lavoro futuro, pattern già pronto (`{leg}`)

## Join

- `senatore_id`: `regexp_extract('/senatore/(\d+)')` → join con `senato_firmatari.senatore_id`
- Nome: label splittata (prima parola = nome, resto = cognome) — attenzione ai nomi composti ("Luca De Carlo" → nome "Luca", cognome "De Carlo"; ok; "Vittorio Emanuele Orlando" → nome "Vittorio", cognome "Emanuele Orlando" — limite noto dello split)

## Limiti

- **Nessun ponte con la Camera**: il Senato non ha `owl:sameAs` Wikidata (verificato: 0) e `senatore_id` ≠ `persona_id` Camera. Il ponte persone Camera↔Senato resta da progettare (join nominativo o via `senato_firmatari.deputato_url`)
- Solo senatori della XIX; il luogo di nascita è la città (non normalizzata a codice ISTAT)
