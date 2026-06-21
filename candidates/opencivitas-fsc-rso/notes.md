# Notes

## Tecnico

- source A: ZIP con CSV singolo `{year}_VAR_FSC_1_{year}.csv`
- source A: CSV con `;` come delimitatore e `,` come separatore decimale
- source A: shape long, una riga per componente di calcolo del fondo
- source B: ZIP con workbook `Metadati_Enti_FSC_2025.xlsx`
- source B: sheet `anagrafica_enti2025`
- chiave di join comune: `USERNAME`
- anni: 2022–2025 (URL pattern `{year}_VAR_FSC_1_{year}_csv.zip`)
- colonne raw per posizione (col0=USERNAME, col1=nome, col2=valore)
  - 2022-2024: VAR_FSC_NAME / VAR_FSC_VAL
  - 2025+: Componenti di calcolo del fondo / Valore
- il clean SQL gestisce entrambi i formati (posizionale)

## Anni

| Anno | URL | Colonne raw |
|:----:|-----|-------------|
| 2022 | `2022_VAR_FSC_1_2022_csv.zip` | USERNAME, VAR_FSC_NAME, VAR_FSC_VAL |
| 2023 | `2023_VAR_FSC_1_2023_csv.zip` | USERNAME, VAR_FSC_NAME, VAR_FSC_VAL |
| 2024 | `2024_VAR_FSC_1_2024_csv.zip` | USERNAME, VAR_FSC_NAME, VAR_FSC_VAL |
| 2025 | `2025_VAR_FSC_1_2025_csv.zip` | USERNAME, Componenti di calcolo del fondo, Valore |

## Analitico

- sei componenti chiave FSC: POPOLAZIONE, CAPACITA_FISCALE, FONDO_PEREQUATIVO,
  DOTAZIONE_FINALE_FSC, IMU_TASI_STANDARD, TOTALE_RISORSE_STORICHE
- `FONDO_PEREQUATIVO` è la metrica di partenza più leggibile
- source B (enti) vive in `support_datasets/` ed è dataset fisso (2025)
- il mart arricchito (`mart_compose_comuni`) include metriche procapite

## Cautele

- perimetro solo RSO (~6.570 comuni): non usare "tutti i comuni italiani"
- Sicilia e Sardegna escluse (hanno solo componente storica)
- il numero di comuni varia leggermente tra anni (~±8)
