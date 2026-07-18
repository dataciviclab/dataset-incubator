# ANAC — Aggiudicatari (support)

**Dataset**: `anac_aggiudicatari`
**Tipo**: support — anagrafica operatori economici aggiudicatari di appalti pubblici
**Fonte**: ANAC — Autorità Nazionale Anticorruzione
**Protocollo**: CKAN (via dati.gov.it)
**Licenza**: CC BY 4.0

## Contenuto

Anagrafica degli operatori economici che si sono aggiudicati appalti ordinari pubblicati su dati.anticorruzione.it. Ogni riga rappresenta un operatore economico associato a un'aggiudicazione.

## Schema (6 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | CIG (join con `anac_bandi_gara`, `anac_aggiudicazioni`) |
| `ruolo` | VARCHAR | Ruolo (OPERATORE ECONOMICO MONOSOGGETTIVO, IMPRESA AUSILIARIA, ecc.) |
| `codice_fiscale` | VARCHAR | Partita IVA / CF dell'operatore |
| `denominazione` | VARCHAR | Ragione sociale |
| `tipo_soggetto` | VARCHAR | Tipo (IMPRESA, DITTA INDIVIDUALE, STAZIONE APPALTANTE, ecc.) |
| `id_aggiudicazione` | BIGINT | ID aggiudicazione (join con `anac_aggiudicazioni`) |

## Join chain

```
anac_bandi_gara (cig) → anac_aggiudicazioni (cig)
anac_aggiudicazioni (id_aggiudicazione) → anac_aggiudicatari (id_aggiudicazione)
```

Join diretto via `cig` anche con `anac_bandi_gara`.

## Limiti

- `codice_fiscale` può essere nullo per operatori esteri
- `id_aggiudicazione` negativo (-1) indica aggiudicazioni senza corrispondenza anagrafica
- `denominazione` può contenere spazi extra o maiuscole incoerenti
