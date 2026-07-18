# ANAC — Partecipanti (support)

**Dataset**: `anac_partecipanti`
**Tipo**: support — anagrafica partecipanti alle gare pubbliche
**Fonte**: ANAC — Autorità Nazionale Anticorruzione
**Protocollo**: CKAN (via dati.gov.it)
**Licenza**: CC BY 4.0

## Contenuto

Anagrafica dei soggetti che partecipano alle gare pubbliche (non solo i vincitori). Ogni riga rappresenta un partecipante associato a un CIG.

A differenza di `anac_aggiudicatari` (solo vincitori), qui ci sono TUTTI i partecipanti: permette analisi di concorrenza, esclusioni, concentrazione.

## Copertura

| Metrica | Valore |
|---|---|
| Righe | ~8M |
| CIG distinti | ~4,7M |
| Partecipanti distinti | ~578K |
| Match con anac_aggiudicazioni | 95% |

## Schema (5 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | CIG (join con `anac_bandi_gara`, `anac_aggiudicazioni`) |
| `ruolo` | VARCHAR | Ruolo del partecipante |
| `codice_fiscale` | VARCHAR | CF / P.IVA del partecipante |
| `denominazione` | VARCHAR | Ragione sociale |
| `tipo_soggetto` | VARCHAR | Tipo (IMPRESA, DITTA INDIVIDUALE, ecc.) |

## Join chain

```
partecipanti (cig) → anac_bandi_gara (cig)
partecipanti (cig) → anac_aggiudicazioni (cig)
partecipanti (codice_fiscale) → anac_aggiudicatari (codice_fiscale)
```

## Limiti

- Stessa struttura di `anac_aggiudicatari` ma include anche i non vincitori
- Full dump non rigenerato frequentemente (file cumulativo 2023+ delta)
