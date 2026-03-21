# Notes

## Tecnico

- source `A`: ZIP con CSV singolo `2025_VAR_FSC_1_2025.csv`
- source `A`: CSV con `;` come delimitatore e `,` come separatore decimale
- source `A`: shape long, una riga per componente di calcolo del fondo
- source `B`: ZIP con workbook `Metadati_Enti_FSC_2025.xlsx`
- source `B`: sheet verificato `anagrafica_enti2025`
- chiave di join comune tra le due fonti: `USERNAME`

## Analitico

- il v0 resta annuale: `2025`
- il primo join deve concentrarsi su sei componenti chiave, senza allargarsi
  subito all’intero schema FSC
- `FONDO_PEREQUATIVO` è la metrica di partenza più leggibile per rispondere alla
  domanda guida
- il mapping anagrafico non è più un support dataset separato: è il source `B`
  del candidate

- il compose minimo vive in `compose/` come layer documentato, ma viene
  eseguito da `sources/a_fsc/sql/mart_compose.sql`

## Cautele

- il perimetro è solo RSO: non usare mai “tutti i comuni italiani”
- prima del join il source `A` resta tecnicamente utile, ma non ancora
  pubblicabile come output leggibile
- l’estensione `2023-2025` va verificata con source-check separato, non va
  presupposta omogenea
