# dait-amministratori-locali

Anagrafe degli Amministratori Locali e Regionali (DAIT) — snapshot corrente (giugno 2026).

**Fonte**: Ministero dell'Interno — Dipartimento per gli Affari Interni e Territoriali
- **URL**: https://dait.interno.gov.it/elezioni/open-data/amministratori-locali-e-regionali-in-carica
- **Download diretto**: https://dait.interno.gov.it/documenti/ammcom.csv (26.7 MB)

## Domanda

*Chi sono gli amministratori locali italiani? Quali profili demografici (età, genere, titolo di studio, professione) hanno sindaci, assessori e consiglieri comunali? Come cambia la composizione della classe politica locale tra territori?*

Sotto-domande esplorative:
- Quante donne sono elette? La presenza femminile varia per carica?
- Qual è l'età media di sindaci, assessori, consiglieri?
- Ci sono differenze territoriali (Nord/Sud) nella composizione?
- Quanto durano in carica i sindaci?

## Dataset

- **Fonte**: `ammcom.csv` — Amministratori Comunali (DAIT)
- **Granularità**: 1 riga = 1 amministratore in 1 carica
- **Periodo**: snapshot corrente (2026)
- **Righe**: 124.716 amministratori in carica
- **Colonne (20)**: anno, codice_regione, codice_provincia, codice_comune, codice_dait_completo, denominazione_comune, sigla_provincia, popolazione_censita, cognome, nome, sesso, data_nascita, luogo_nascita, descrizione_carica (Sindaco/Assessore/Consigliere/...), incarico, data_elezione, data_entrata_in_carica, lista_appartenenza, titolo_studio, professione

## Mart

| Mart | Descrizione |
|---|---|
| `mart_profilo_carica` | Conteggi, età media, % femmine/maschi per carica |
| `mart_profilo_demografico` | Distribuzione sesso × classe di età per carica |
| `mart_territorio` | Composizione per regione × carica (quota femmine, età media) |

Rispondono alle domande del README: profilo demografico della classe politica locale, presenza femminile per carica, differenze territoriali.

## Esecuzione

```bash
cd dataset-incubator
toolkit run -c candidates/dait-amministratori-locali/dataset.yml
```

## Issue di riferimento

- Intake: [#349](https://github.com/dataciviclab/dataset-incubator/issues/349)
