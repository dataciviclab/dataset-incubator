# ipa-unita-organizzative

**Support dataset** — Unità Organizzative (UO) della PA italiana.

## Descrizione

Anagrafica completa delle Unità Organizzative delle pubbliche amministrazioni e dei gestori di pubblici servizi, dall'Indice dei domicili digitali della PA (IPA).

Ogni UO è identificata da `codice_uni_uo` e può dipendere gerarchicamente da un'altra UO tramite `codice_uni_uo_padre`, consentendo la ricostruzione di alberi organizzativi fino a 9 livelli di profondità.

## Fonte

- **Ente**: AgID — Agenzia per l'Italia Digitale
- **URL**: https://dati.gov.it/opendata/dataset/f3834cff-f1bb-4344-9536-15b5a1c393a5
- **Licenza**: CC BY 4.0
- **Aggiornamento**: Continuo (IPA)

## Copertura

- **122.470 UO** per **23.530 enti** (su ~23.709 iscritti IPA)
- Snapshot 2026
- **35.367 UO (29%)** con gerarchia esplicita (codice_uni_uo_padre valorizzato)
- Profondità massima: **9 livelli**

## Schema chiave

| Colonna | Tipo | Descrizione |
|---|---|---|
| `codice_ipa` | VARCHAR | FK → ipa_enti.codice_ipa |
| `codice_uni_uo` | VARCHAR | PK — identificativo univoco UO |
| `codice_uni_uo_padre` | VARCHAR | FK verso sé stessa (UO superiore) |
| `codice_uni_aoo` | VARCHAR | FK → ipa_aree_organizzative_omogenee |
| `descrizione_uo` | VARCHAR | Nome UO (es. "Ufficio Tecnico") |
| `nome_responsabile` | VARCHAR | Nome del responsabile |
| `cognome_responsabile` | VARCHAR | Cognome del responsabile |
| `data_istituzione` | VARCHAR | Data istituzione UO (yyyy-mm-dd) |

## Uso nel Lab

- Join con `ipa_enti` per contesto ente
- Join con `dipendenti_pubblici` per personale per ufficio
- Join con `anac_bandi_gara` per appalti per ufficio
- CTE ricorsiva per ricostruzione albero gerarchico
