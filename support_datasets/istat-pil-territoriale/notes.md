# Notes: istat_pil_territoriale

## Domanda guida
Support dataset per normalizzazione PIL e Valore Aggiunto territoriale.

## Stato operativo (2026-10-11)

- **Canale**: toolkit `type: sdmx` (canale diretto esploradati) — remigrazione
  post-fix toolkit key SDMX (#444). Il mirror dbnomics era un'edizione
  indietro (2025M6, max 2023): audit collegato a #873
- **Dataset**: `IT1/93_498` v1.0 · B1GQ / B1G / D21X31 · VALUATION=V · ADJUSTMENT=N
- **Copertura**: nazionale/macro-aree/regioni 1995–2024 (edizione 2025M12);
  province ~2000–2023. L'edizione è esplicita nel raw, il clean fa `arg_max`
  con ordinamento numerico YYYYMmm (max su stringa sbaglia: "2025M12" < "2025M6")
- **Metriche**: solo PIL, VA, imposte nette. Niente branche ATECO.

## Rate limit ISTAT

ISTAT SDMX: **~5 query al minuto**, ban temporanei. Il fetch è single-shot
(1 request + retries/backoff del plugin); in caso di 429 il run va riprovato.

## Rischi noti

1. **Edizioni multiple**: clean prende max(EDITION) per REF_AREA × DATA_TYPE_AGGR
2. **Break di serie**: conti economici con cambi metodologici; qui solo prezzi correnti
3. **Extra-Regio (ITZ)**: se presente, gestire separatamente per PIL regionale puro
4. **Province storiche**: geografia corrente nel dato

## Trigger per estensione

- Valore aggiunto per branca ATECO → vedi experiment `istat-va-branca` (93_1227)
- PIL concatenato (L_2020) per serie reali
- Dati trimestrali

## Label territoriali (2026-10-11)

`territorio` / `territorio_nome` usano un **CASE NUTS statico** nel clean
(codelist ESTAT GEO, nomi italiani). NUTS stabili — aggiornamento solo se
cambiano confini. Codici ISTAT IT1xx (province post-2004, non in GEO 2021) (`IT108`–`IT111`)
mappati: IT108=Monza e della Brianza, IT109=Fermo, IT110=Barletta-Andria-Trani, IT111=Sud Sardegna. Aggregati ISTAT (`ITCD`, `ITDA`,
`ITFG`, `ITCDE`) mappati a label descrittive.
