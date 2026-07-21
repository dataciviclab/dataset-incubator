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

Se tocchi `candidates/`:

- [ ] `dataset.yml` presente con `name` e `years`
- [ ] toolkit run eseguito senza errori su tutti gli anni dichiarati
- [ ] nessun file dati committato nella root del candidate (`*.csv`, `*.parquet`, `*.xlsx`)
- [ ] output immagini cleared dal notebook (rimuovere `image/png`)
- [ ] notebook nominato `{slug}_v0.ipynb`, nessun path assoluto di macchina
- [ ] issue di intake collegata
- [ ] `sql/clean.sql` usa le **macro standard del toolkit** dove applicabile (`normalize_string`, `cast_int`, `cast_double`, `normalize_italian_number`, `decode_flag` — vedi toolkit/docs/standard-macros.md)

## Verifica

Spiega come hai verificato il cambiamento.

```bash
# Esempi
python -m toolkit.cli.app run all --config candidates/{slug}/dataset.yml
python scripts/validate_candidate_structure.py
```

- [ ] `run all` o `dry-run` eseguito senza errori (candidate/support)
- [ ] `python scripts/validate_candidate_structure.py` passato
- [ ] Perimetro stretto: candidate con domanda minima chiara

## Note / rischi

Rischi, limiti, punti da controllare con attenzione.
