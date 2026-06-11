## Tecnico

- **Fonte**: DAIT — snapshot corrente CSV via HTTP
- **URL diretto**: `https://dait.interno.gov.it/documenti/ammcom.csv`
- **Protocollo**: HTTP file (non CKAN)
- **CSV**: UTF-8, delim `;`, header alla riga 3 (prime 2 righe = metadati da skippare)
- **Dimensione raw**: 26.68 MB
- **Colonne**: 18 colonne raw → 19 clean (aggiunta `anno`)
- **Granularità**: amministratori comunali

## Run

- **Dataset**: ammcom.csv (amministratori comunali, snapshot 2026)
- **Run ID**: `20260611T103450Z_bb4522c9`
- **Esito**: SUCCESS (7.7s)
- **Righe clean**: 116.054
- **Readiness**: 5/5

## Confronto altri CSV DAIT

I 6 CSV disponibili nella pagina open-data hanno schemi DIVERSI tra loro. Non unificabili automaticamente con `mode: all`:

| CSV | Colonne | Unione con ammcom? |
|---|---|---|
| `ammcom.csv` | 18 (schema base) | — |
| `maggiororgano.csv` | 18 (identico) | ✅ UNION diretto |
| `ammprov.csv` | 17 (+ data_elezione_max_carica, - codice_comune) | ❌ schema diverso |
| `ammmetropolitani.csv` | 17 (come ammprov) | ❌ schema diverso |
| `ammreg.csv` | 14 (solo regione) | ❌ schema ridotto |
| `organistraordinariincarica.csv` | 11 (solo base) | ❌ schema ridotto |

Per unire file con schemi diversi servirebbe clean.sql manuale con UNION ALL e aliasing colonne.

## Analitico

- `codice_regione`, `codice_provincia`, `codice_comune`: codici ISTAT (leading zero perso nel cast INTEGER)
- `denominazione_comune`, `sigla_provincia`: dati territoriali
- `popolazione_censita_alla_data_elezione`: popolazione al momento dell'elezione (spesso NULL se non aggiornata)
- `cognome`, `nome`, `sesso`: anagrafica (M/F) — sesso quasi sempre valorizzato
- `data_nascita`: formato DD/MM/YYYY nel raw, mantenuto come VARCHAR nel clean
- `luogo_nascita`: comune di nascita (es. "ACQUI TERME (AL)")
- `descrizione_carica`: valori osservati → Sindaco, Assessore, Consigliere, Consigliere candidato sindaco
- `incarico`: sub-ruolo opzionale (Vicesindaco, Presidente del consiglio, ecc.)
- `data_elezione`, `data_entrata_in_carica`: date in formato DD/MM/YYYY (VARCHAR nel clean)
- `lista_appartenenza/collegamento`: nome della lista elettorale (rinominata in `lista_appartenenza` nel clean)
- `titolo_studio`: categorizzazione amministrativa (es. "Laurea Magistrale", "Istruzione Secondaria di Secondo Grado")
- `professione`: classificazione ISTAT-like delle professioni (es. "IMPRENDITORI TITOLARI E AMMIN. DELEGATI DI IMPRESE COMMERCIALI")

## Cautele

- **Encoding**: i CSV attuali sono UTF-8, ma versioni passate usavano latin1 — verificare per serie storica
- **Skip rows**: prime 2 righe = metadati ("Amministratori Comunali...", "Aggiornato al..."). Gestito con `clean.read.skip: 2`
- **Colonna con slash**: `lista_appartenenza/collegamento` richiede quoting DuckDB (`"lista_appartenenza/collegamento"`). Rinominata a `lista_appartenenza` nel clean
- **Popolazione censita**: spesso NULL se il comune non ha aggiornato il dato
- **Professione/titolo_studio**: categorizzazioni amministrative verbose — da normalizzare in analisi
- **Lista appartenenza**: formato libero, nomi molto lunghi e concatenati con `|` — richiede pulizia NLP
- **Parallel scanner**: DuckDB richiede `parallel: false` con `null_padding: true` (righe con quoted newlines)
- **Auto-inferenza tipi**: disabilitata con `columns` espliciti VARCHAR per evitare errori su date/campo popolazione
- **Serie storica**: snapshot annuali hanno struttura e naming diversi tra anni → da verificare consistenza
- **Dimensione**: 26.7 MB gestibile (~3 MB Parquet)
- **Stato SO**: fonte `dait` è in `radar-only` — dopo intake si può valutare `catalog-watch`
