# dait-amministratori-locali

Anagrafe degli Amministratori Locali e Regionali (DAIT) — snapshot corrente (giugno 2026).

**Fonte**: Ministero dell'Interno — Dipartimento per gli Affari Interni e Territoriali
- **URL**: https://dait.interno.gov.it/elezioni/open-data/amministratori-locali-e-regionali-in-carica
- **Download diretto**: https://dait.interno.gov.it/documenti/ammcom.csv (26.7 MB)

## Domanda

*Chi sono gli amministratori locali italiani? Quali profili demografici (età, genere, titolo di studio, professione) hanno sindaci, assessori e consiglieri comunali? Come cambia la composizione della classe politica locale tra territori e nel tempo?*

Sotto-domande esplorative:
- Quanto durano in carica i sindaci? Ci sono differenze Nord/Sud?
- Quali professioni prevalgono tra gli amministratori locali?
- Quante donne sono elette? La presenza femminile aumenta nel tempo?
- Qual è l'età media di sindaci, assessori, consiglieri per regione?

## Dataset

- **Fonte**: `ammcom.csv` — Amministratori Comunali (DAIT)
- **Granularità**: 1 riga = 1 amministratore in 1 carica
- **Periodo**: snapshot corrente (2026). In futuro → serie storica 1991–2025
- **Righe**: 116.054 amministratori in carica
- **Colonne (19)**: anno, codice_regione, codice_provincia, codice_comune, denominazione_comune, sigla_provincia, popolazione_censita, cognome, nome, sesso, data_nascita, luogo_nascita, descrizione_carica (Sindaco/Assessore/Consigliere/Consigliere candidato sindaco), incarico (Vicesindaco, Presidente del consiglio, ecc.), data_elezione, data_entrata_in_carica, lista_appartenenza, titolo_studio, professione

## Mart

| Mart | Descrizione |
|---|---|
| `dait_amministratori_locali` | Tutti gli amministratori (schema flat, passthrough) |

Mart aggiuntivi (`dait_sindaci`, `dait_amministratori_territorio`) da sviluppare in fase successiva.

## Perché vale la pena incubarlo

- **Primo dataset "anagrafico" del Lab**: primo dataset con persone fisiche (nome, cognome, età, professione, titolo di studio)
- **Domanda civica forte e trasversale**: la composizione della classe politica locale interessa cittadini, giornalisti, ricercatori
- **Alto valore di join**: si aggancia a tutti i dataset comunali del Lab (IRPEF, rifiuti, popolazione, FSC, ecc.) via codice_comune × anno
- **Unico nel catalogo**: nessun altro dataset dà il profilo socio-demografico dei politici locali
- **Serie storica lunghissima**: 1991–2026 = 35 anni di dati, permette analisi di trend (fase 2)
- **Fonte ufficiale e strutturale**: Ministero dell'Interno, aggiornamento annuale

## Output minimo atteso

- ✅ Tabella clean `dait_amministratori_locali` — 116.054 righe, 19 colonne
- ✅ Run full RAW→CLEAN→MART superato (7.7s, readiness 5/5)
- ✅ Notebook v0 con setup candidate
- ⬜ Mart dimensionale territoriale (fase 2)
- ⬜ Serie storica 1991–2025 (fase 2)

## Criterio di promozione

Superato il **review readiness** con run full (RAW→CLEAN→MART) su anno 2026:
- `config_valid` ✅
- `raw_output_present` ✅
- `clean_output_readable` ✅ (116.054 righe)
- `mart_outputs_readable` ✅
- `run_record_coherent` ✅

## Stato

- intake

## Prossimo passo

- review PR e merge
- eventuale estensione con `maggiororgano.csv` (sindaci) via inject_column
- serie storica 1991–2025
