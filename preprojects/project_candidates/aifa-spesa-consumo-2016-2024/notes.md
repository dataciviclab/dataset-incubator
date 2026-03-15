# Notes

## Tecnico

- 9 file annuali: 2016-2024, ~31 MB/anno, ~174k righe/anno (dato 2023)
- formato: CSV pipe-separated (`|`), encoding UTF-8-BOM
- granularita: anno x mese x 21 regioni/PA x classe x ATC4
- due flussi distinti nello stesso file con null strutturali:
  - `convenzionata`: prescrizioni SSN dispensate in farmacia
  - `tracciabilita`: acquisti diretti / ospedaliero / DPC / prontuario H
- perimetro iniziale: solo `convenzionata` (colonne `spesa_convenzionata`, `numero_confezioni_convenzionata`)
- i file vanno scaricati manualmente dalla pagina AIFA e rinominati:
  `aifa_spesa_consumo_{year}.csv` in `out/data/raw/aifa_spesa_consumo/{year}/`

**URL di download per anno (da pagina AIFA ufficiale):**

- 2016: `https://www.aifa.gov.it/documents/20142/847578/dati2016_100519.csv/c6e2e4d7-2663-92ad-6554-c3668e581b2d`
- 2017: `https://www.aifa.gov.it/documents/20142/847578/dati2017_100519.csv/f4db1267-05c1-b65c-7a04-11633ff0a215`
- 2018: `https://www.aifa.gov.it/documents/20142/847578/dati2018_23.09.2020.csv`
- 2019: `https://www.aifa.gov.it/documents/20142/847578/dati2019_23.09.2020.csv`
- 2020: `https://www.aifa.gov.it/documents/20142/847578/dati2020_22.10.2021.csv`
- 2021: `https://www.aifa.gov.it/documents/20142/847578/dati2021_24.10.2022.csv`
- 2022: `https://www.aifa.gov.it/documents/20142/847578/dati2022_07.02.2024.csv`
- 2023: `https://www.aifa.gov.it/documents/20142/847578/dati2023_15.01.2025.csv`
- 2024: `https://www.aifa.gov.it/documents/20142/847578/dati2024_04.12.2025.csv`

**Nota URL**: gli URL contengono token non parametrici — non automatizzabili con `{year}`.
Scaricare manualmente. Se gli URL cambiano a un nuovo aggiornamento, riprendere dalla pagina ufficiale.

**Nomi colonna approssimati (da verificare sul primo run):**
- identificativi: `anno`, `mese`, `codreg`, `regione`
- gerarchia terapeutica: `classe`, `atc1`, `desc_atc1`, `atc2`, `desc_atc2`, `atc3`, `desc_atc3`, `atc4`, `desc_atc4`
- flusso convenzionata: `numero_confezioni_convenzionata`, `spesa_convenzionata`
- flusso tracciabilita: `numero_confezioni_traccia`, `spesa_flusso_tracciabilita`

**Manuale AIFA irraggiungibile.** Il link "Manuale Operativo" sulla pagina AIFA punta a
`Cover-Letter-Europass-20181126-Porcaro-IT.pdf` (link rotto, non e il documento tecnico).
I nomi colonna sono stati verificati direttamente sul file 2023 e risultano stabili su 2022-2024.
Schema da riverificare quando si aggiungono gli anni 2016-2021.

## Risultati primo run (2022-2024)

Run completato su 3 anni. Tutti i layer clean + mart hanno passato la validazione.

| anno | righe clean | righe mart |
|------|-------------|------------|
| 2022 | 91.850 | ~78k |
| 2023 | 92.654 | 78.802 |
| 2024 | 92.129 | ~78k |

Totale convenzionata 2023 (nazionale): 9,87 mld EUR

Top 5 ATC4 per spesa 2023 (nazionale):
- A02BC Inibitori pompa protonica: 652,7 mln EUR
- C10AA Statine (HMG CoA reduttasi): 476,1 mln EUR
- R03AK Adrenergici + corticosteroidi (asma/BPCO): 390,8 mln EUR
- C07AB Betabloccanti selettivi: 300,3 mln EUR
- C09CA ARBs anti-ipertensivi: 294,6 mln EUR

Top 5 regioni spesa convenzionata 2023:
Lombardia 1,86 mld - Campania 1,04 mld - Lazio 1,03 mld - Sicilia 0,83 mld - Puglia 0,72 mld

Gate 1 parzialmente risolto: nomi colonna verificati sul file reale.
Il manuale AIFA resta irraggiungibile (link rotto), ma il tracciato e interpretabile.

## Analitico

- domanda principale: come cambia la spesa convenzionata per ATC4 tra regioni e nel tempo?
- taglio iniziale: flusso `convenzionata` aggregato per `anno x mese x regione x atc4`
- metriche minime: `spesa_convenzionata`, `numero_confezioni_convenzionata`, quota % sul totale regionale
- domande complementari:
  - quali regioni spendono di piu pro capite per cardiovascolari?
  - dove crescono di piu gli antidiabetici tra 2016 e 2024?
  - ci sono classi in calo strutturale (biosimilari, genericazione)?
- attenzione: i totali regionali assoluti non sono comparabili senza normalizzazione per popolazione
- non sommare convenzionata + tracciabilita nella prima analisi: sono canali diversi

## Cautele

- la spesa assoluta non e comparabile tra regioni senza dati di popolazione
- i null nelle colonne dei due flussi sono strutturali, non errori di parsing
- `codreg` potrebbe non allinearsi direttamente ai codici ISTAT standard senza lookup
- eventuali aggiornamenti retroattivi dei file AIFA non sono segnalati esplicitamente:
  i file hanno timestamp nel nome (es. `dati2022_07.02.2024.csv`) che indica la data di rilascio,
  non la copertura — tenere traccia della versione scaricata
- ATC4 e il livello massimo disponibile in questo dataset (niente AIC o ATC5)
- nessun dettaglio sub-regionale (ASL, distretto, comune)
