# ipa-enti

Anagrafica completa delle pubbliche amministrazioni e gestori di pubblici servizi
dall'Indice dei domicili digitali della PA (IPA) — fonte AgID.

## Fonte

- **URL**: https://indicepa.gov.it/ipa-dati/dataset/enti
- **Licenza**: CC-BY-4.0
- **Aggiornamento**: giornaliero
- **Formato originale**: XLSX → dump CSV via DataStore

## Campi principali

| Colonna | Descrizione |
|---|---|
| `codice_ipa` | Identificativo unico IPA |
| `denominazione_ente` | Nome ufficiale ente |
| `codice_fiscale_ente` | CF ente |
| `tipologia` | PA, Stazione Appaltante, Gestore, ecc. |
| `mail1`...`mail5` | Indirizzi email |
| `tipo_mail1`...`tipo_mail5` | Tipologia email (Pec/Altro) |
| `sito_istituzionale` | Sito web ufficiale |
| `nome/cognome/titolo_responsabile` | Vertice ente |
| `codice_comune_istat` | Codice ISTAT comune sede |
| `data_aggiornamento` | Data ultimo aggiornamento |

## Uso

Usato da `data-advocacy` per alimentare l'anagrafica enti con PEC e contatti
certificati IPA.
