# Note — ameco

## Source-check

- Ispezione locale 2026-10-09 (`esperimenti-locali/ameco-benchmark/NOTES.md`): zip scaricato, struttura verificata, overlap con Lab documentato.
- Fonte non registrata in source-observatory (source_id `ec_ameco` dichiarato ad-hoc, precedente: `fts`, `ted`).
- Decisione perimetro: lean (6 serie × 6 paesi) per evitare duplicazione con `pil-intelligence` e `eurostat-debito-pil`.

## Rischi tecnici / quirks della fonte

- **Wide format**: 18 CSV con colonne-anno 1960..2027 + colonna residua `Unnamed: 73` (artefatto pandas nell'export). Esclusa nel clean.
- **NA letterali**: valori mancanti = stringa `NA`, non vuoto. Gestiti con `CASE ... WHEN 'NA' THEN NULL`.
- **Varianti unità nel CODE**: stesso suffisso serie con unità diverse (es. `UDGG` in Mrd EUR, %PIL, PPS). Il clean filtra l'unità corretta per ciascuna serie (vedi commenti in `clean.sql`).
- **UBLGAPS vs UBLGAP**: `UBLGAPS` è la variante seasonally adjusted — esclusa dal filtro (match esatto sul suffix).
- **Suffisso .R**: alcune serie hanno suffisso `R` (relative performance) — non nel perimetro lean.
- **Snapshot unico**: `years: [2026]` = release Spring 2026. Rilasci futuri (Autumn 2026, …) = nuova run con `output_policy: overwrite`. Non c'è serie multi-release nel v0 (vintage archive = follow-up).
- **tipo_dato**: `previsione` se anno ≥ 2025 per questa release. Soglia specifica della release Spring 2026 (2025 = anno corrente della forecast). Cambia con release successive — aggiornare la costante in `clean.sql` se si passa ad Autumn/N+1.

## Decisioni metodologiche

- **Perimetro lean**: 6 serie (ZUTN, UVGD, UBLG, UDGG, UBLGAP, ADGGI) × 6 paesi (IT, DE, FR, ES, EU27, EA20). Esclude la duplicazione con Eurostat osservato; include previsioni + ciclico + snowball.
- **Unità fisse per serie**: UVGD in Mrd ECU/EUR (unit 99), UBLG/UDGG/UBLGAP in %PIL EDP (unit 319), ZUTN/ADGGI unit 0. Motivato da confrontabilità nel mart.
- **primary_key clean**: `[paese, serie, anno]` — un valore per cella; verificata la unicità sui dati locali.
- **Soglia previsioni**: `anno >= 2025` per Spring 2026. Non derivabile dal dato (AMECO non marca le colonne forecast) — dipende dalla release, documentato qui e in clean.sql.

## Overlap noto (non bloccante)

- Parte osservata di UVGD/UBLG/UDGG sovrappone parzialmente `pil-intelligence` (Eurostat NAMA_10_GDP) e `eurostat-debito-pil` (gov_10dd_edpt1). Accettato: il candidate è complementare (previsioni + ciclico), non primario. Nessun import cross-dataset nel v0.
