# Note tecniche — EU Call Open (SEDIA)

## Fonte

- **API**: `POST https://api.tech.ec.europa.eu/search-api/prod/rest/search?apiKey=SEDIA`
- **apiKey**: `SEDIA` è il letterale pubblico inviato dal frontend EC — non è un secret
- **Formato**: multipart con 3 blob: `query` (bool JSON), `languages` (`["en"]`), `sort`
- ⚠️ Body JSON puro **non filtra** `status` correttamente — multipart obbligatorio
- **Facet**: `POST .../rest/facet` stesso pattern (per risolvere codici opachi)
- **Licenza**: EU Open Data / dati del portale UE
- Probe locale: `_local/probe/sedia/` nel workspace (2026-10-12)

## Codici (verificati 2026-10-12)

| Campo | Valori usati |
|---|---|
| `type` | `1` = grant topics |
| `status` | `31094501` Forthcoming · `31094502` Open · `31094503` Closed |
| `programmePeriod` | `"2021 - 2027"` |

Dizionario `frameworkProgramme` parziale in `extract_sedia.py` (`FRAMEWORK_LABELS`) — espandibile via facet.

## Pipeline

- `type: script` → `extract_sedia.py` (stdlib: urllib + csv + json)
- Dedup su `identifier` (la search può restituire record multipli per action)
- Anno run: `[2026]` (snapshot corrente, non serie storica)

## Volumi probe (2026-10-12)

| Status | api_total | deadline future |
|---|---|---|
| Open | 352 | ~111 |
| Forthcoming | 651 | ~299 |
| Open+forthcoming | 1003 | ~409 |

## ⚠️ Status non affidabile da solo

~2/3 degli "Open" ha `deadlineDate` **passata** (dato non aggiornato sul portale).
Il clean marca `ha_scadenza_futura` e il mart espone solo le future.

## Budget

Dentro `budgetOverview` (stringa JSON): sommare `budgetYearMap` per anno.
`maxContribution` può essere 0 con importo reale altrove — non usarlo come totale.

## Rischio API non ufficiale

È il backend del frontend del portale: nessun versioning promesso.
Mitigazione: script isolato, colonne minime, notes con data di probe.
Se l'API cambia: fallisce il run raw, non il resto del Lab.

## Catena con FTS

`fts_eu_grants` espone `call_id`/`project_id` (2020-2023 e 2025).
Join teorico: `fts.call_id = eu_call_open.call_identifier` — solo su call
chiusi/progetti assegnati, non sugli open topic di questo dataset.

## Non fare

- Non usare `text=` vuoto senza multipart (totalResults gonfiati)
- Non paginare senza dedup `identifier`
- Non filtrare per Italia sui topic (EU-wide)
