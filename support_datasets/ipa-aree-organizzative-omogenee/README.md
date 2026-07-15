# ipa-aree-organizzative-omogenee

**Support dataset** — Aree Organizzative Omogenee (AOO) della PA italiana.

## Descrizione

Anagrafica delle Aree Organizzative Omogenee di cui agli artt. 50 e 61 del D.P.R. n. 445/2000, corrispondenti ai registri di protocollo dell'ente. Ogni AOO raggruppa le Unità Organizzative (UO) per area omogenea e dispone di un proprio domicilio digitale.

## Fonte

- **Ente**: AgID — Agenzia per l'Italia Digitale
- **URL**: https://dati.gov.it/opendata/dataset/c1a4e530-fd1f-433a-a2ef-62e9862a9a6a
- **Licenza**: CC BY 4.0
- **Aggiornamento**: Continuo (IPA)

## Copertura

- **39.380 AOO** per **21.769 enti**
- Snapshot 2026

## Schema chiave

| Colonna | Tipo | Descrizione |
|---|---|---|
| `codice_ipa` | VARCHAR | FK → ipa_enti.codice_ipa |
| `codice_uni_aoo` | VARCHAR | PK — identificativo univoco AOO |
| `denominazione_aoo` | VARCHAR | Nome dell'area (es. "Area Amministrativa") |
| `nome_responsabile` | VARCHAR | Nome del responsabile |
| `cognome_responsabile` | VARCHAR | Cognome del responsabile |
| `data_istituzione` | VARCHAR | Data istituzione AOO |
| `protocollo_informatico` | VARCHAR | Indicatore presenza protocollo informatico |
| `uri_protocollo_informatico` | VARCHAR | URI del servizio di protocollo |
| `cod_aoo` | VARCHAR | Codice AOO assegnato dall'ente |

## Uso nel Lab

- Join con `ipa_unita_organizzative` via `codice_uni_aoo` per raggruppamento UO per area
- Join con `ipa_enti` per contesto ente
- Classificazione della struttura organizzativa per macrocategoria
