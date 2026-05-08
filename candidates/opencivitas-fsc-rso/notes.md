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
- il primo join si concentra su sei componenti chiave FSC, senza allargarsi
  subito all'intero schema
- `FONDO_PEREQUATIVO` è la metrica di partenza più leggibile per rispondere alla
  domanda guida
- source `B` (opencivitas_fsc_enti_rso) vive in `support_datasets/` ed è dichiarato
  come `support:` in `dataset.yml`
- il compose FSC+enti arricchito di geografia vive in `sql/mart_compose.sql` ed è
  l'unica mart table del candidate

## Cautele

- il perimetro è solo RSO: non usare mai "tutti i comuni italiani"
- l'estensione `2023-2025` va verificata con source-check separato, non va
  presupposta omogenea
