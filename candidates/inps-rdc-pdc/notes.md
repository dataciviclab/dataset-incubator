## Tecnico

- Granularita rilevata: comune (7.976 comuni)
- Fonte: INPS Open Data, CSV singolo (ID-5773)
- Join key: `codice_istat` (ISTAT comune)
- Encoding: utf-8, delim: `,`, skip: 0

## Analitico

- Unico anno: luglio 2020 (singolo snapshot)
- 18 colonne: dati RdC/PdC per comune + popolazione residente + takeup
- Importo medio mensile: ~449€ media nazionale
- Popolazione max: Roma 2.808.293, min: comuni soppressi (0)

## Anomalie note (dati INPS originali, non errori di clean)

1. **Nomi comuni**: lowercase senza spazi (es. "abanoterme", "abbadiacerreto") — così nel CSV INPS originale
2. **Popolazione = 0**: ~5 comuni con popolazione 0 (Acquarica del Capo, Alice Superiore, Auditore, Barberino Val d'Elsa, Berra) — sono codici ISTAT di comuni soppressi/fusi prima del 2020
3. **Importo medio con 0 nuclei RDC+PdC**: 620 comuni hanno importo medio > 0 ma 0 nuclei RdC e 0 PdC — artefatto del dataset INPS (possibile media su finestra diversa)

## Cautele

- Singolo anno (2020): non c'è serie storica
- Dati INPS aggiornati a luglio 2020 — verificare se esistono snapshot successivi
- Join via codice_istat: alcuni codici potrebbero non corrispondere all'anagrafe ISTAT corrente
