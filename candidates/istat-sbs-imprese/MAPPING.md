# Mappatura del dataflow SBS

Dataflow nazionale: `ISTAT/161_267_DF_DCSP_SBSNAZ_1`.

- **118** `DATA_TYPE` disponibili.
- **20** estratti nel dataset: 11 core + 9 quartili.
- **98** documentati ma non estratti: varianti granulari (fatturato per attività,
  investimenti per asset, quartili di altri indicatori). Per attivarne uno basta
  aggiungere il codice alla lista `DATA_TYPE` in `dataset.yml`.

Dimensioni:

- `ECON_ACTIVITY_NACE_2007`: sezioni B–S + codici 10/11/12/47 per le filiere.
- `PERS_EMPL_SIZE_CLASS`: `TOTAL` + `W0_9`, `W10_19`, `W20_49`, `W50_249`,
  `W_GE250` per i core nazionali; `TOTAL` per quartili e regionale.
- `TURNOVER_CLASS=9`, `ENVIROM_DOMAIN=9`.
- Anni: 2008–2024; quartili 2013–2024.

Unità: `mila_eur` = migliaia di euro; `migliaia_ore` = migliaia di ore;
`conte` = numero; `pct` = percentuale; `indice` = indice/rapporto.

## Indicatori estratti

| Codice | Etichetta | Unità | Uso |
|---|---|---|---|
| `12110` | Fatturato | mila_eur | Margini, dimensione |
| `12120` | Valore della produzione | mila_eur | Produzione |
| `12150` | Valore aggiunto al costo fattore | mila_eur | Produttività, quota lavoro |
| `12170` | Risultato lordo di gestione | mila_eur | GOS/VA |
| `13310` | Costi del personale | mila_eur | Quota lavoro, ULC |
| `13320` | Salari e stipendi | mila_eur | Costo del lavoro |
| `13330` | Contributi sociali | mila_eur | Composizione costo |
| `15110` | Investimenti fissi lordi | mila_eur | Investimenti/VA |
| `16150` | Ore lavorate dai dipendenti | migliaia_ore | Produttività oraria |
| `11110` | Imprese | conte | Numerosità |
| `11210` | Unità locali | conte | Numerosità |
| `E12150_PER_ADD_Q1/Q2/Q3` | VA per addetto, quartili | mila_eur | Distribuzione dentro il settore |
| `E13310_PER_DIP_Q1/Q2/Q3` | Costo del personale per dipendente, quartili | mila_eur | Distribuzione dentro il settore |
| `N00001_Q1/Q2/Q3` | Wage-adjusted labour productivity, quartili | indice | Trasmissione produttività-salari |

## Codebook completo (118 DATA_TYPE)

| Codice | Etichetta DBnomics | Unità | Perimetro |
|---|---|---|---|
| `11101` | revenue from sale of products manufactured by the enterprise  (thousands of euros) | mila_eur | documentato |
| `11102` | revenue from sale of goods and services (thousands of euros) | mila_eur | documentato |
| `11105` | revenue from intermediate activity ( thousands of euros) | mila_eur | documentato |
| `11106` | revenue from gross incomes on the transport (thousands of euros) | mila_eur | documentato |
| `11107` | revenue from services to third parties (thousands of euros) | mila_eur | documentato |
| `11110` | enterprises | conte | core |
| `11210` | local units | conte | core |
| `11400` | increase of fixed assets for internal works (thousands of euros) | mila_eur | documentato |
| `11500` | others operative revenues (thousands of euros) | mila_eur | documentato |
| `12100` | purchases of raw materials and goods (thousands of euros) | mila_eur | documentato |
| `12101` | purchases of raw materials (thousands of euros) | mila_eur | documentato |
| `12110` | turnover (thousands of euros) | mila_eur | core |
| `12120` | production value  (thousands of euros) | mila_eur | core |
| `12130` | gross margin on goods for resale ( thousands of euros) | mila_eur | documentato |
| `12150` | value added at factor cost (thousands of euros) | mila_eur | core |
| `12170` | gross operating surplus  (thousands of euros) | mila_eur | core |
| `12200` | purchases of services ( thousands of euros) | mila_eur | documentato |
| `12300` | payment for enjoyment goods owned by third parties (thousands of euros) | mila_eur | documentato |
| `12900` | others  operating costs (thousands of euros) | mila_eur | documentato |
| `13110` | total purchases of goods and services ( thousands of euros) | mila_eur | documentato |
| `13111` | purchases of goods: raw materials and goods for resale or consumption in the production process (thousands of euros) | mila_eur | documentato |
| `13112` | purchases of services including other business services provided by third parties (thousands of euros) | mila_eur | documentato |
| `13120` | purchases of goods and services purchased for resale in the same condition as received (thousands of euros) | mila_eur | documentato |
| `13131` | payments for agency workers (thousands of euros) | mila_eur | documentato |
| `13210` | change in stocks of goods and services (thousands of euros) | mila_eur | documentato |
| `13211` | change in stocks of goods and services purchased for resale in the same condition as received  (thousands of euros) | mila_eur | documentato |
| `13213` | change in stocks of finished products and work in progress manufactured by the unit (thousands of euros) | mila_eur | documentato |
| `13310` | personnel costs (thousands of euros) | mila_eur | core |
| `13320` | wages and salaries (thousands of euros) | mila_eur | core |
| `13330` | social security costs (thousands of euros) | mila_eur | core |
| `13411` | payments for long term rental and operational leasing of goods (thousands of euros) | mila_eur | documentato |
| `15110` | gross investment in tangible goods (thousands of euros) | mila_eur | core |
| `15120` | gross investment in land (thousands of euros) | mila_eur | documentato |
| `15130` | gross investment in existing buildings and structures (thousands of euros) | mila_eur | documentato |
| `15140` | gross investment in construction and alteration of buildings (thousands of euros) | mila_eur | documentato |
| `15150` | gross investment in machinery and equipment (thousands of euros) | mila_eur | documentato |
| `15210` | sales of tangible investment goods (thousands of euros) | mila_eur | documentato |
| `15420` | gross investment in concessions, patents, licences, trade marks and similar rights (thousands of euros) | mila_eur | documentato |
| `15441` | investment in purchased software (thousands of euros) | mila_eur | documentato |
| `16110` | persons employed | conte | documentato |
| `16130` | employees | conte | documentato |
| `16140` | employees (in full time equivalent units) | conte | documentato |
| `16150` | hours worked by employees (thousands) | migliaia_ore | core |
| `18100` | turnover from agriculture, forestry, fishing and industrial activities  (thousands of euros) | mila_eur | documentato |
| `18110` | turnover from the principal activity (thousands of euros) | mila_eur | documentato |
| `18120` | turnover from industrial activities (thousands of euros) | mila_eur | documentato |
| `18121` | turnover from industrial activities excluding construction (thousands of euros) | mila_eur | documentato |
| `18122` | turnover from construction (thousands of euros) | mila_eur | documentato |
| `18150` | turnover from service activities (thousands of euros) | mila_eur | documentato |
| `18160` | turnover from trading activities and from intermediary activities (thousands of euros) | mila_eur | documentato |
| `18310` | turnover from building (thousands of euros) | mila_eur | documentato |
| `18320` | turnover from civil engineering (thousands of euros) | mila_eur | documentato |
| `20110` | purchases of energy products (thousands of euros) | mila_eur | documentato |
| `21110` | investment in equipment and plant for pollution control and special anti-pollution accessories (mainly end-of-pipe equipment) (thousands of euros) | mila_eur | documentato |
| `21120` | investment in equipment and plant linked to cleaner technology (integrated technology) (thousands of euros) | mila_eur | documentato |
| `21140` | gross investment in other tangible goods (thousands of euros) | mila_eur | documentato |
| `23110` | payments to sub-contractors(thousands of euros) | mila_eur | documentato |
| `23120` | income from sub-contracting (thousands of euros) | mila_eur | documentato |
| `31001` | persons employed - women | conte | documentato |
| `31100` | entrepeneurs, owners, cooperators | conte | documentato |
| `31200` | managers, clerks | conte | documentato |
| `31300` | workers | conte | documentato |
| `31400` | homeworkers | conte | documentato |
| `31500` | apprentices | conte | documentato |
| `33333` | employees - women | conte | documentato |
| `51500` | gross investment in course and payments on account (migliaia di euro) | mila_eur | documentato |
| `80001` | gross investment in construction, buildings and structures (migliaia di euro) | mila_eur | documentato |
| `80002` | gross investment in machinery and equipment (thousands of euros) | mila_eur | documentato |
| `80003` | gross investment in fornitures and others equipments (thousands of euros) | mila_eur | documentato |
| `80004` | gross investment in vehicle for transport (thousands of euros) | mila_eur | documentato |
| `80005` | gross investment in other tangible goods (thousands of euros) | mila_eur | documentato |
| `E12110_PER_ADD_Q1` | turnover per person employed -   1° quartile  (thousand of euros) | mila_eur | documentato |
| `E12110_PER_ADD_Q2` | turnover per person employed -    2° quartile  (thousand of euros) | mila_eur | documentato |
| `E12110_PER_ADD_Q3` | turnover per person employed - 3° quartile  (thousand of euros) | mila_eur | documentato |
| `E12110_PER_ADD_STD` | turnover per person employed - standard deviation (thousand of euros) | mila_eur | documentato |
| `E12110_Q1` | turnover -  1° quartile  (thousand of euros) | mila_eur | documentato |
| `E12110_Q2` | turnover -  2° quartile (thousand of euros) | mila_eur | documentato |
| `E12110_Q3` | turnover -  3° quartile (thousand of euros) | mila_eur | documentato |
| `E12110_STD` | turnover -  standard deviation (thousand of euros) | mila_eur | documentato |
| `E12150_PER_ADD_Q1` | value added per person employed  -  1° quartile (thousand of euros) | mila_eur | quartili |
| `E12150_PER_ADD_Q2` | value added per person employed  - 2° quartile (thousand of euros) | mila_eur | quartili |
| `E12150_PER_ADD_Q3` | value added per person employed  - 3° quartile (thousand of euros) | mila_eur | quartili |
| `E12150_PER_ADD_STD` | value added per person employed - standard deviation (thousand of euros) | mila_eur | documentato |
| `E12150_Q1` | value added - 1° quartile  (thousand of euros) | mila_eur | documentato |
| `E12150_Q2` | value added - 2° quartile  (thousand of euros) | mila_eur | documentato |
| `E12150_Q3` | value added -  3° quartile  (thousand of euros) | mila_eur | documentato |
| `E12150_STD` | value added - standard deviation (thousand of euros) | mila_eur | documentato |
| `E12150_SU_FATT_Q1` | value added divided by turnover -   1° quartile  (percentage) | pct | documentato |
| `E12150_SU_FATT_Q2` | value added divided by turnover  - 2° quartile  (percentage) | pct | documentato |
| `E12150_SU_FATT_Q3` | value added divided by turnover  - 3° quartile  (percentage) | pct | documentato |
| `E12150_SU_FATT_STD` | value added divided by turnover - standard deviation (percentage) | pct | documentato |
| `E12170_Q1` | gross operating surplus -  1° quartile (thousand of euros) | mila_eur | documentato |
| `E12170_Q2` | gross operating surplus -  2°  quartile (thousand of euros) | mila_eur | documentato |
| `E12170_Q3` | gross operating surplus - 3° quartile (thousand of euros) | mila_eur | documentato |
| `E12170_STD` | gross operating surplus - standard deviation  (thousand of euros) | mila_eur | documentato |
| `E13310_PER_DIP_Q1` | personnel costs per employee - 1° quartile (thousand of euros) | mila_eur | quartili |
| `E13310_PER_DIP_Q2` | personnel costs per employee -  2° quartile (thousand of euros) | mila_eur | quartili |
| `E13310_PER_DIP_Q3` | personnel costs per employee - 3° quartile (thousand of euros) | mila_eur | quartili |
| `E13310_PER_DIP_STD` | personnel costs per employee - standard deviation  (thousand of euros) | mila_eur | documentato |
| `E13310_Q1` | personnel costs - 1° quartile (thousand of euros) | mila_eur | documentato |
| `E13310_Q2` | personnel costs - 2°  quartile (thousand of euros) | mila_eur | documentato |
| `E13310_Q3` | personnel costs - 3° quartile (thousand of euros) | mila_eur | documentato |
| `E13310_STD` | personnel costs - standard deviation  (thousand of euros) | mila_eur | documentato |
| `E16110_Q1` | persons employed -1° quartile | conte | documentato |
| `E16110_Q2` | persons employed - 2° quartile | conte | documentato |
| `E16110_Q3` | persons employed - 3° quartile | conte | documentato |
| `E16110_STD` | persons employed - standard deviation | conte | documentato |
| `E16130_Q1` | employees - 1° quartile | conte | documentato |
| `E16130_Q2` | employees - 2°  quartile | conte | documentato |
| `E16130_Q3` | employees -  3° quartile | conte | documentato |
| `E16130_STD` | employees - standard deviation | conte | documentato |
| `N00001_Q1` | wage adjusted labour productivity - 1° quartile | indice | quartili |
| `N00001_Q2` | wage adjusted labour productivity - 2° quartile | indice | quartili |
| `N00001_Q3` | wage adjusted labour productivity - 3° quartile | indice | quartili |
| `N00001_STD` | wage adjusted labour productivity - standard deviation | indice | documentato |
| `NUM_CON_ADD` | interprises with persons employed | conte | documentato |
| `NUM_CON_DIP` | enterprises with employees | conte | documentato |
| `NUM_CON_FATT` | enterprises where turnover more than zero | conte | documentato |
