# personale-ssn

## Issue
DataCivicLab/dataset-incubator#454

## Fonte dati
Ministero della Salute — https://www.dati.salute.gov.it/
Dataset "Personale del SSN" - https://www.dati.salute.gov.it/dataset/personale-del-ssn.jsp

## File raw
- 2010-2019: `C_17_dataset_65_0_upFile.xls` (formato XLS multi-foglio, contiene tutti gli anni)
- 2020: `C_17_dataset_120_0_upFile.xlsx` (formato XLSX)
- 2021: `C_17_dataset_191_0_upFile.xlsx` (formato XLSX)

## Schema clean
15 colonne: prospetto (TAB1 / MEDICI_E_INFERMIERI), anno, codice_regione, denominazione_regione, codice_azienda, ruolo_categoria, dotazioni_organiche, tempo_pieno_u/d, part_time_inf_50_u/d, part_time_sup_50_u/d, pers_anno_rif_u/d

## Prospetti
- **TAB1**: totale personale per macro-categoria (S=Sanitario, T=Tecnico, A=Amministrativo, P=Professioni)
- **MEDICI_E_INFERMIERI**: dettaglio di "S" (Sanitario) — medici e infermieri separati
- Relazione: TAB1.S = MEDICI + INFERMIERI + altro personale sanitario
- Il mart usa solo TAB1 per il totale (MEDICI_E_INFERMIERI è un sottoinsieme)

## Cross-reference con BDAP
Stock personale 2021 — confronto con `dipendenti-pubblici` (BDAP/RGS):

| Fonte | Comparto | Stock |
|-------|----------|-------|
| BDAP | SANITÀ | 670.637 |
| Personale SSN (TAB1) | — | 648.491 |

Differenza ~3.3%, fisiologica per diverse classificazioni (Ministero Salute vs RGS).
Quota SSN su totale PA: ~20% (648K su 3.24M).

## Note tecniche
- Il file XLS per 2010-2019 contiene fogli TAB1_YYYY e MED E INF_YYYY per ogni anno
- I file XLSX per 2020-2021 hanno fogli "TAB1 YYYY" e "MED E INF_YYYY"
- Il mart aggrega solo TAB1 (categoria S include già medici e infermieri)
- Cache dei file raw in `cache/` (gitignorato)
- Il preprocess.py riceve l'anno via CLI ma processa sempre l'intera serie 2010-2021
  (pattern single-year con time_coverage full_series)
