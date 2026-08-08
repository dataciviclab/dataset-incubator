# mef-rappresentanti-partecipate

**Domanda guida:** Quanto vengono pagati i rappresentanti della PA nei CdA delle partecipate?

**Fonte:** MEF — Dipartimento del Tesoro
**URL:** https://www.de.mef.gov.it/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni/
**Formato:** CSV (ISO-8859-1, delimitatore `;`)
**Copertura:** 2018–2023 (6 anni)
**Licenza:** CC BY 4.0

## Schema output (29 colonne)

| Blocco | Colonne |
|--------|---------|
| 📅 **Anno** | `anno` |
| 🏛️ **Amministrazione** | `amministrazione`, `amm_settore`, `amm_macrocategoria`, `amm_categoria`, `amm_cf`, `amm_regione`, `amm_provincia`, `amm_comune` |
| 🏢 **Società** | `societa`, `societa_cf`, `societa_anno_costituzione`, `societa_forma_giuridica`, `societa_stato`, `societa_settore`, `societa_ateco`, `societa_regione`, `societa_provincia`, `societa_comune` |
| 👤 **Rappresentante** | `rapp_id`, `rapp_cognome`, `rapp_nome`, `rapp_genere` |
| 📋 **Incarico** | `incarico_tipo`, `incarico_data_inizio`, `incarico_data_fine`, `incarico_gratuito`, `incarico_importo_eur`, `incarico_riversato_eur` |

## Esecuzione

```bash
cd dataset-incubator
python -m toolkit.cli.app run all \
  --config candidates/mef-rappresentanti-partecipate/dataset.yml
```

## Issue di riferimento

- Intake: [#544](https://github.com/dataciviclab/dataset-incubator/issues/544)

## Perché vale la pena

I compensi dei rappresentanti della PA nei CdA delle società partecipate sono soldi pubblici: 132,9 milioni € nel 2023. Sapere chi nomina, chi viene pagato, quanto e con quale divario di genere è una domanda di trasparenza diretta — risponde alla discussion #406 (11 domande verificate sul dato).

## Output minimo atteso

- `mart_trend_anno`: spesa PA per anno (109,7M → 132,9M, +21% in 6 anni), quota gratuiti, riversato
- `mart_sintesi_incarico`: compenso medio per ruolo (AD €63.923 = 6x consigliere)
- `mart_gender_gap`: divario di genere per anno (F = 68% del compenso M)
- `mart_top_amministrazioni`: chi nomina e paga di più (MEF, Roma, Milano)

## Criterio di promozione

Promuovere quando: (1) i numeri del trend e del gender gap sono verificati e citabili; (2) almeno una risposta della discussion #406 è chiusa con dati; (3) la geografia dei compensi (Nord-Sud) è esplorata via query SQL.

## Stato / prossimo passo

- **Stato**: candidate a standard v1 (2026-08-03) — 4 mart serie, run passed 6 anni, readiness 8/8
- **Prossimo passo**: merge PR; post-merge: catalog aggiornamento; rispondere alle domande #406 con le mart
