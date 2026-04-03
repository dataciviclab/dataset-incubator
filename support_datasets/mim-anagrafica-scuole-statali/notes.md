# Notes

## Tecnico

- fonte CSV diretta su `catalogo/elements1/`, non sul path legacy `catalog/`
- file v0 intake: `SCUANAGRAFESTAT20242520250831.csv`
- header presente e leggibile nel probe HTTP reale
- chiave di join: `CODICESCUOLA`
- per coerenza con `mim-alunni-corso-eta`, il support v0 resta sullo stesso anno scolastico `2024/25`

## Analitico

- dataset infrastrutturale prima che narrativo
- serve a collegare la granularità scuola con comune/provincia/regione
- non va usato come base autonoma di letture pubbliche senza un dataset principale

## Cautele

- le anagrafiche scolastiche cambiano nel tempo; evitare join cross-year nel v0
- `DESCRIZIONECOMUNE` e `PROVINCIA` sono descrittivi; `CODICESCUOLA` resta la chiave primaria di lavoro
