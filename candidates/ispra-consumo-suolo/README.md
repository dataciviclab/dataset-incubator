# ispra-consumo-suolo

**Domanda guida:** Quali territori continuano a consumare piu suolo, e quanto pesa ancora il consumo recente rispetto allo stock gia accumulato?

**Fonte:** ISPRA — Consumo di suolo, dataset nazionale 2006-2024
**Formato:** XLSX (foglio Comuni_2006_2024)
**Granularita:** comune

**Issue di riferimento:** [dataset-incubator #32](https://github.com/dataciviclab/dataset-incubator/issues/32), [dataset-incubator #70](https://github.com/dataciviclab/dataset-incubator/issues/70)

## Come eseguire

```bash
cd dataset-incubator
toolkit/.venv/Scripts/python.exe -m toolkit.cli.app run all \
  --config candidates/ispra-consumo-suolo/sources/a_consumo_suolo/dataset.yml
```

## Output

- `out/data/mart/ispra_consumo_suolo/2024/mart_comuni.parquet`

## Nota dati

Il `clean` e il `mart` espongono ora tutti gli incrementi netti e lordi per periodo presenti nel foglio ISPRA `Comuni_2006_2024`.

I periodi non sono uniformi:
- `2006-2012`
- `2012-2015`
- poi annuali fino a `2023-2024`

Questi campi vanno quindi letti come sequenza di intervalli eterogenei, non come serie annuale gia normalizzata.
