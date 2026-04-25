# Note tecniche — irpef-comunale

## Fonte

ZIP annuali ufficiali MEF / Finanze:
`https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_{year}.zip`

## Copertura temporale

2019–2023 (5 anni di dichiarazione)

## Copertura territoriale

Tutti i comuni italiani (~7.900 per anno). I codici ISTAT sono stabili nel tempo.

## Struttura raw

| Anno | Colonne CSV raw | Note |
|---|---|---|
| 2019 | 50 | Header: `Bonus spettante` (col 26-27) |
| 2020 | 50 | Header: `Bonus spettante` (col 26-27) |
| 2021 | 50 | Header: `Trattamento spettante` (col 26-27) — nuovo |
| 2022 | 50 | Header: `Trattamento spettante` (col 26-27) |
| 2023 | 52 | Aggiunte `Reddito complessivo` (col 34-35) + `Trattamento spettante` |

## Struttura clean

52 colonne fisse per tutti gli anni (slot 0–51). Le colonne assenti nel raw originale hanno valore NULL:
- **col 26–27**: `Bonus spettante` per 2019-2020 (NULL dal 2021); `Trattamento spettante` per 2021-2023 (NULL nel 2019-2020)
- **col 34–35**: `Reddito complessivo` solo per 2023 (assenti = NULL per 2019-2022)

Il clean è raw-faithful: nessuna logica interpretativa, nessun case/when, nessuna colonna derivata. Il consumatore vede esattamente cosa c'è nel raw per ogni anno.

## Schema clean (52 colonne)

```
0  anno_di_imposta
1  codice_catastale
2  codice_istat_comune
3  denominazione_comune
4  sigla_provincia
5  regione
6  codice_istat_regione
7  numero_contribuenti
8  reddito_da_fabbricati_freq
9  reddito_da_fabbricati_eur
10 reddito_da_lavoro_dipendente_e_assimilati_freq
11 reddito_da_lavoro_dipendente_e_assimilati_eur
12 reddito_da_pensione_freq
13 reddito_da_pensione_eur
14 reddito_da_lavoro_autonomo_comprensivo_valori_nulli_freq
15 reddito_da_lavoro_autonomo_comprensivo_valori_nulli_eur
16 reddito_di_spettanza_imprenditore_contabilita_ordinaria_freq
17 reddito_di_spettanza_imprenditore_contabilita_ordinaria_eur
18 reddito_di_spettanza_imprenditore_contabilita_semplificata_freq
19 reddito_di_spettanza_imprenditore_contabilita_semplificata_eur
20 reddito_da_partecipazione_freq
21 reddito_da_partecipazione_eur
22 reddito_imponibile_freq
23 reddito_imponibile_eur
24 imposta_netta_freq
25 imposta_netta_eur
63  trattamento_spettante_freq          ← contiene Bonus spettante per 2019-2020 (semantica diversa — vedi Limiti); NULL per 2021-2023
64  trattamento_spettante_eur            ← contiene Bonus spettante per 2019-2020 (semantica diversa — vedi Limiti); NULL per 2021-2023
28 reddito_imponibile_addizionale_freq
29 reddito_imponibile_addizionale_eur
30 addizionale_regionale_dovuta_freq
31 addizionale_regionale_dovuta_eur
32 addizionale_comunale_dovuta_freq
33 addizionale_comunale_dovuta_eur
34 reddito_complessivo_freq             ← NULL per 2019-2022 (introdotto nel 2023)
35 reddito_complessivo_eur             ← NULL per 2019-2022 (introdotto nel 2023)
36 reddito_complessivo_minore_o_uguale_a_zero_euro_freq
37 reddito_complessivo_minore_o_uguale_a_zero_euro_eur
38–51 reddito_complessivo_da_NN_a_MM_euro (fasce freq+eur)
```

## Limiti e caveat

- **Bonus vs Trattamento**: il MEF ha sostituito il Bonus Covid con il Trattamento (legge 2021). Le due misure non sono direttamente confrontabili come semantica economica — il Bonus era un credito d'imposta una tantum, il Trattamento è un importo erogato. Non sommarle mai come "spettante totale".
- **Reddito complessivo** (2023): non esiste nei precedenti — non è ricostruibile dai raw precedenti.
- **Frequenze vs ammontare**: le frequenze (colonne `*_freq`) per le fasce di reddito complessivo (col 38-51) sono conteggi di contribuenti, non valori monetari. Non hanno corrispondente euro.
- **Somalettura regionale**: la somma dei comuni può non coincidere con il totale regionale (dati.flags rettifiche, segreti comunali, variazioni anagrafiche). I totali regionali vanno chiesti direttamente al MEF.
- **Anno di imposta vs anno di dichiarazione**: i dati si riferiscono all'anno di imposta, non all'anno di presentazione della dichiarazione. Di norma c'è un anno di ritardo.

## Note di ingest / clean

- Il raw usa `normalize_rows_to_columns: true` + `skip: 1` per estrarre la riga header come nomecolonne, poi `header: false` per leggere i dati. Le colonne vengono poi rinominate esplicitamente nel clean.sql.
- Il CSV usa `;` come delimitatore e `;` finale su ogni riga (che genera una colonna vuota added). Il `trim_whitespace: true` gestisce gli spazi extra.

## Note analitiche iniziali

- Il dataset è la base più completa per confrontare la capacità fiscale comunale e regionale in Italia.
- Le tabelle mart (`irpef_by_regione`, `irpef_by_comune`) offrono una vista già aggregata pronta per analisi.
- Il `mart_multi_anno` include rank nazionali/regionali e delta vs anno precedente.
- `popolazione_comune` è assente dal clean (era nel vecchio clean come placeholder per join futuro — il join con `support_datasets/popolazione-istat-comunale-2019-2025` è l'anello mancante per arricchire le analisi pro-capite).
