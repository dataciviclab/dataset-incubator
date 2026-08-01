## Sintesi

Descrivi in poche righe cosa cambia e perché.

## Contesto collegato

Closes #

## Cosa cambia

- [ ] candidate — nuovo dataset o aggiornamento
- [ ] support — dataset di supporto
- [ ] docs — struttura candidate, README, template
- [ ] cleanup — refactoring, rimozioni, allineamento
- [ ] workflow o CI
- [ ] altro

## Impatto

Segna solo quello che si applica.

- [ ] Aggiunge o modifica un candidate / support in `candidates/`
- [ ] Modifica la struttura attesa dei candidate (dataset.yml, cartelle)
- [ ] Cambia il contratto con consumatori downstream (explorer, analisi)
- [ ] Solo documentazione o metadati
- [ ] Nessun impatto visibile per chi usa il repository

## Checklist candidate

Se tocchi `candidates/` (standard: `docs/candidate-standard.md`):

- [ ] `dataset.yml` con `name`, `years`, `source_id`, `tags`, `category` (tutti obbligatori — gate strict)
- [ ] `clean.validate` con `required_columns`, `not_null`, `min_rows` (primary_key se dichiarabile)
- [ ] `mart.validate.table_rules` con `primary_key` dai GROUP BY
- [ ] `toolkit run` eseguito senza errori su tutti gli anni dichiarati
- [ ] `python scripts/validate_candidate_structure.py` passato senza failure
- [ ] nessun file dati committato nella root del candidate (`*.csv`, `*.parquet`, `*.xlsx`)
- [ ] output immagini cleared dal notebook (rimuovere `image/png`)
- [ ] notebook nominato `{slug}_v0.ipynb`, nessun path assoluto di macchina
- [ ] issue di intake collegata
- [ ] `sql/clean.sql` usa le **macro standard del toolkit** dove applicabile (`normalize_string`, `cast_int`, `cast_double`, `normalize_italian_number`, `decode_flag` — vedi toolkit/docs/standard-macros.md)

## Verifica

Spiega come hai verificato il cambiamento.

```bash
# Esempi
toolkit run -c candidates/{slug}/dataset.yml --years 2024
python scripts/validate_candidate_structure.py
python scripts/batch_by_source.py --fonte <source_id>   # preflight per fonte
```

- [ ] `toolkit run` eseguito senza errori (candidate/support)
- [ ] `python scripts/validate_candidate_structure.py` passato
- [ ] Perimetro stretto: candidate con domanda minima chiara

## Note / rischi

Rischi, limiti, punti da controllare con attenzione.
