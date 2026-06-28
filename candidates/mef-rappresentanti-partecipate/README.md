# mef-rappresentanti-partecipate

**Domanda guida:** Quanto vengono pagati i rappresentanti della PA nei CdA delle partecipate?

**Fonte:** MEF — Dipartimento del Tesoro
**URL:** https://www.de.mef.gov.it/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni/
**Formato:** CSV (ISO-8859-1, delimitatore `;`)
**Copertura:** 2018–2023 (6 anni)
**Licenza:** CC BY 4.0

## Schema output (28 colonne)

| Blocco | Colonne |
|--------|---------|
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
