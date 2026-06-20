# Elezioni Politiche 2022 — risultati per comune

Risultati delle elezioni politiche del 25 settembre 2022 (Camera dei Deputati e Senato della Repubblica) a livello comunale.

**117.591 righe per la Camera**, **117.510 per il Senato**: ogni riga rappresenta il voto a una lista in un comune, con il candidato uninominale associato. 7.824 comuni coperti.

## I dati

Il dataset contiene 19 colonne che permettono di analizzare il voto per:
- **comune** — denominazione
- **lista elettorale** — descrizione (es. "FRATELLI D'ITALIA CON GIORGIA MELONI")
- **candidato uninominale** — nome, cognome, data e luogo nascita, sesso
- **collegio** — plurinominale e uninominale
- **elettori e votanti** — totali e per genere, schede bianche
- **voti** — alla lista e al candidato uninominale

### Camera (C)
| Metrica | Valore |
|---|---|
| Righe | 117.591 |
| Comuni | 7.824 |
| Liste | 23 |
| Media voti per lista | 230 |

### Senato (S)
| Metrica | Valore |
|---|---|
| Righe | 117.510 |
| Comuni | 7.545 |
| Liste | 22 |
| Media voti per lista | 226 |

Nota: Camera e Senato hanno un diverso numero di comuni per via dell'elettorato attivo (over 18 per Camera, over 25 per Senato) e delle differenze nella rappresentanza della Valle d'Aosta.

## Cross con altri dataset

| Dataset | Chiave | Domanda |
|---|---|---|
| `irpef_comunale` | comune (testo) | I comuni ricchi votano diversamente? |
| `dait_amministratori_locali` | comune | Il colore dell'amministrazione corrisponde al voto? |
| `popolazione_istat_comunale` | comune | L'astensione è correlata all'età della popolazione? |
| `ispra_ru_base` | comune | I comuni virtuosi nell'ambiente votano verde? |

## Fonte

**Eligendo** — Archivio storico elettorale del DAIT (Ministero dell'Interno)
URL: https://elezionistorico.interno.gov.it/eligendo/opendata.php
Licenza: CC BY 4.0

## Issue

#523 — Intake eligendo: serie storica elezioni
