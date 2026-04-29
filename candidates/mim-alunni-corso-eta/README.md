# MIM alunni per corso ed età

## Domanda

- Quali territori mostrano il calo più forte di iscritti nelle scuole primarie statali?
- Qual è la pressione demografica scolastica per ordine e regione?

## Dataset

- fonte principale: MIM `Alunni per corso ed età`
- support dataset: `SCUANAGRAFESTAT` (anagrafica scuole statali)
- download: automatizzato via `url_suffix_by_year` in `dataset.yml`
- anni disponibili: **2016-2025** (10 anni scolastici)
- URL list page: `https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Studenti&datasetId=DS0010ALUCORSOETASTA`
- licenza dichiarata: `IODL 2.0`

## Perché vale la pena incubarlo

- granularità a livello `CODICESCUOLA` + join con anagrafica
- 10 anni di serie storica — trend demografico solido
- forte leggibilità civica sul calo iscrizioni
- il blocco `support:` del toolkit rende dichiarativo il join con l'anagrafica scuole

## Output minimo atteso

- raw: CSV per anno scolastico (2016-2025)
- clean: tabella normalizzata con `CODICESCUOLA`, ordine, anno di corso, fascia età e numero alunni — raw-faithful
- mart: 4 aggregati per comune (primaria, sec_I, sec_II, all) — filtri ordine nel mart SQL
- notebook v0 per sanity check mart

## Stato

`runnable` — 2016-2025 run completo, raw-faithful, 4 mart verificate

## QC

- Clean = Raw su tutti gli anni (0% drop) ✅
- Mart sum = Clean: perfetto per 2025 (delta=0, anagrafica 2024 copre tutte le scuole); delta crescente per anni precedenti (scuole chiuse/fuse assenti dall'anagrafica) — comportamento atteso, non errore ✅
- 4 mart: tutte superano min_rows su tutti gli anni ✅

## Criterio di promotion

- mart comunale stabile come base di join con anagrafica
- notebook v0 eseguito con output reali (2024/25)
