# art-taxi-ncc

**Licenze TAXI e NCC per comune (2024)** — ART, Autorità di Regolazione dei Trasporti.

Fonte: https://bdt.autorita-trasporti.it/wp-content/uploads/dcat/D32-Diffusione-TAXI-NCC-2024-v2.csv
Issue intake: #665

## Domanda

Quali comuni italiani hanno più taxi e NCC in rapporto alla popolazione? Dove il mercato è più concentrato o assente?

## Dataset

- **Copertura**: 176 comuni con licenze, snapshot 2024
- **Colonne**: comune, taxi, ncc, popolazione_residente
- **Volumi**: 23.501 licenze TAXI, 5.228 NCC
- **Mart**: `mart_taxi_ncc_per_capite` con ratio ogni 10.000 residenti

## Perché vale la pena

- Self-contained: la popolazione è già nel dataset, ratio calcolabile subito
- Quality score toolkit: 96/100
- Incrociabile con ACI (parco veicolare) e MIT (incidentalità)

## Output minimo atteso

Clean parquet + mart per-capite. Top per taxi/10k: Taormina (39,3), Milano (35,5), Roma (28,0).

## Stato

- [x] scaffold + run raw/clean/mart (validate ok)
- [ ] PR + review
