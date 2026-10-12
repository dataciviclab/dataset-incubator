# ISTAT SBS — Imprese per settore NACE

## Domanda

- Quali settori NACE generano più fatturato e valore aggiunto in Italia?
- Come si distribuiscono tra Italia e regioni?

## Dataset

- fonte: ISTAT via DBnomics (`type: dbnomics`)
- dataflow nazionale: `161_267_DF_DCSP_SBSNAZ_1`
- dataflow regionale: `161_268_DF_DCSP_SBSREG_1`
- indicatori: fatturato (12110), valore aggiunto (12150), produzione (12120), costi personale (13310), unità locali (11210)
- unità monetarie: **migliaia di euro** (`valore / 1000 = mln €`)
- grano: Italia + 21 regioni NUTS1 × NACE sezioni B–S

## Perché vale la pena

- confronto nazionale/regionale dello stesso indicatore SBS
- grano NACE sezione, utile per policy industriali
- serie storica 2008–2023

## Output

- `mart_sbs_anno`: `anno × territorio × grain × NACE × indicatore`
