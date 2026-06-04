# reparti-ricovero

Dataset del Ministero della Salute — Dati di struttura e attività dei reparti di ricovero.

**Fonte**: https://www.dati.salute.gov.it/it/dataset/dati-di-struttura-e-di-attivita-dei-reparti-presenti-ciascuna-struttura-di-ricovero
**URL diretto CSV**: `Dati_di_anagrafe_e_di_attività_delle_Strutture_di_Ricovero_Pubbliche_ed_equiparate.csv`
**Anno**: 2022
**Licenza**: CC BY 4.0

**Domanda**: Offerta di posti letto per disciplina e reparto a livello regionale.

**Output**: `mart_regioni.parquet` (aggregato regionale) e `mart_regioni_disciplina.parquet` (per disciplina).
Non entra nel compose principale di malasanita (ridondante rispetto a C sui posti letto).
