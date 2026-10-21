## Fonte: perché Eurostat e non la CNA

Il portale open data della Commissione Nazionale per il Diritto d'Asilo non esiste più:

- `https://asylum-opendata.dlci.interno.it/` → HTTP 200 ma body di 11 byte (`- Matera -`),
  `robots.txt` di 27 byte; `/open-data-2`, `/open-data`, `/catalogo`, `/it`, `/api`,
  `/sitemap.xml` → 404. È un vhost placeholder.
- Il sito era un WordPress con brand **dati.cna.it** (link nel menu "Open Data" →
  `/open-data-2/`, "Catalogo" → `/catalogo/`, "Esplora i dati" → `/esplora-dati/`).
  `dati.cna.it` non risolve più; `asylum.dlci.interno.gov.it` è NXDOMAIN.
- Web Archive: catturati solo asset WordPress (crawl 2023-06) e la home; **nessun**
  CSV/JSON e `/catalogo/` mai archiviato. Nessun mirror GitHub.
- `dati.gov.it`: nessun dataset CNA (57 risultati per "asilo" sono asili nido/comunali).
- Il sito DLCI pubblica solo PDF aggregati (`/temi/i-numeri-dellasilo`). Verificati con
  `pdfplumber`: riepiloghi 2013-2022, confronti annuali e "Quaderno statistico
  1990-2020" (88 pagine) **non** contengono tabelle per Commissione Territoriale.

Da qui il pivot su Eurostat, che copre domande + esiti per cittadinanza ma **non** la
granularità per Commissione Territoriale.

## Tecnico

- Due dataflow con dimensioni diverse (`decision` vs `applicant`): il toolkit legge un
  solo file raw, quindi `preprocess.py` scarica entrambi e li normalizza in un CSV tidy
  (`misura`, `anno`, `cittadinanza_codice`, `cittadinanza`, `dettaglio_codice`, `valore`).
- `type: script` richiede `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` (già impostato nel workflow
  post-merge). Il file `raw_input.csv` è in `.gitignore`.
- TSV Eurostat: dimensioni separate da virgola, anni separati da tab. L'intestazione
  riporta `geo\TIME_PERIOD`: il suffisso va rimosso per ottenere i nomi delle dimensioni.
- Valori mancanti (`:` o cella vuota) → riga omessa; valori numerici → `BIGINT`.
- Robustezza script: deduplica su `(misura, anno, cittadinanza, dettaglio)` (la PK del
  clean è garantita), scrittura atomica (`.tmp` + rename), errore esplicito se l'API
  risponde XML invece di TSV, fail-fast sui 4xx (retry solo su 429/5xx), sanity check su
  numero anni (≥15), cittadinanze (≥100) e misure attese.
- `SSEQ` (domande reiterate) è pubblicato da Eurostat **solo dal 2021**. Per il 2008-2020
  il mart deriva `domande_reiterate = totale − prima istanza` e lo segnala con
  `reiterate_derivate = true`; dal 2021 il valore è quello pubblicato e
  `reiterate_derivate = false`. Dove entrambi esistono la derivazione coincide con `SSEQ`
  (scarti ±5 per arrotondamento a 5).
- Eurostat arrotonda le celle a multipli di 5 per riservatezza: `POS` può differire da
  `POS_RFG + POS_SPROT + POS_HUM` di ±5 (verificato: max |scarto| = 5 su 444 casi).
- Etichette cittadinanza dal codelist `CITIZEN` (inglese, fedeltà alla fonte). Il codice
  ISO2 è la chiave di join.
- Aggregati esclusi dai mart (`aggregato = true`): i codici che non sono a due lettere
  (`TOTAL`, `EU27_2020`, `EXT_EU27_2020`, `UK_OCT`, `UNK`), con eccezione per `RNC`
  (recognised non-citizens) e `STLS` (apolidi), che sono categorie di persone. La regola
  è calcolata in SQL e copre automaticamente eventuali nuovi codici aggregati; resta un
  criterio euristico (non una validazione ISO-3166), perché `UK`, `EL` e `XK` sono paesi
  pur non essendo codici ISO.
- `mart_asilo_italia` usa la riga `TOTAL` (che include `UNK` e l'arrotondamento a 5),
  mentre `mart_asilo_annuale` esclude gli aggregati: la somma per cittadinanza non
  coincide col totale nazionale. Esempio 2024: 158.375 + 225 `UNK` ≈ 158.605.
- Snapshot unico (`years: [2026]`), serie completa 2008-2025 scaricata in un colpo.

## Analitico — scarto con il dato ufficiale CNA

Confronto 2022 (riepilogo CNA vs Eurostat):

| Voce | CNA | Eurostat |
|---|---|---|
| Domande | 84.289 | 84.290 |
| Decisioni | 58.478 | 53.060 |
| Accolte | 25.678 | 25.680 |
| Dinieghi | 32.800 | 27.385 |

Le **accolte coincidono**, i **dinieghi Eurostat sono inferiori di ~5.400** (2021:
−8.363). Il tasso di riconoscimento Eurostat (48,4% nel 2022) è quindi sovrastimato
rispetto al dato CNA (43,9%). Ipotesi: Eurostat non conteggia alcune decisioni negative
(inammissibilità/Dublino) che la CNA include nei "dinieghi". Non correggibile lato
fonte: il mart espone il dato Eurostat, il confronto con i PDF CNA resta il riferimento
ufficiale per i totali nazionali.

## Cautele

- Granularità per Commissione Territoriale **non disponibile**: nessuna fonte pubblica
  la espone più.
- 2025 è l'ultimo anno pubblicato (dato annuale consolidato); eventuali revisioni
  Eurostat non sono tracciate.
- "Domande" = applicazioni registrate nell'anno, non persone fisiche distinte (una
  persona può presentare domanda reiterata).
- Tasso calcolato su decisioni dell'anno, non sulla coorte di domande dello stesso anno:
  non è un tasso di accoglimento per coorte.
