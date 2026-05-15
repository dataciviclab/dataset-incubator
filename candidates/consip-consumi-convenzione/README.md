# Consip — consumi in convenzione: geografia della spesa delle PA

## Domanda guida

Come si distribuisce geograficamente la spesa delle PA in convenzione Consip?
Quali regioni, province e tipologie di PA concentrano i consumi di energia e utility acquistati tramite convenzioni pubbliche?

## Fonte

- **Ente**: Consip SpA / MEF
- **Portale**: [dati.consip.it](https://dati.consip.it)
- **Dataset**: CONSUMI GENERATI TRAMITE ORDINI DIRETTI DI ACQUISTO IN CONVENZIONE
- **Formato**: CSV, delimitato `,`, encoding utf-8
- **Anni disponibili**: 2023, 2024, 2025
- **Aggiornamento**: annuale (file nominato per anno di edizione)
- **Licenza**: CC-BY-4.0

## Perimetro

- **Periodo**: 2023-2025 (3 anni)
- **Granularità**: lotto-convenzione-provincia-PA (una riga = consumo aggregato per coppia PA-convenzione-lotto)
- **Chiavi territoriali**: regione PA, provincia PA, sigla provincia, regione fornitore
- **Cosa contiene**: consumi economici di energia e utility (elettricità, gas, carburanti) acquistati tramite ordini diretti in convenzione Consip

## Output minimo atteso

- `clean_input`: 12 colonne normalizzate, schema stabile cross-year
- `mart_consumi_convenzione`: aggregazione geografica per anno, regione, provincia, tipologia PA

## Boundary clean/mart

- **Clean**: rename colonne, cast tipi, conversione virgola→punto per decimali. Nessuna aggregazione.
- **Mart**: somma valore consumi, conteggio ordini/PA/PO per dimensione geografica. Nessun join esterno.

## Schema

| Colonna | Tipo | Descrizione |
|---|---|---|
| `anno_riferimento` | INTEGER | Anno di riferimento del consumo |
| `tipologia_amministrazione` | VARCHAR | Tipologia PA (Comune, Università, ASL, etc.) |
| `regione_pa` | VARCHAR | Regione della PA acquirente |
| `provincia_pa` | VARCHAR | Provincia della PA acquirente |
| `sigla_provincia_pa` | VARCHAR | Sigla provincia (2 char) |
| `regione_fornitore` | VARCHAR | Regione del fornitore |
| `convenzione` | VARCHAR | Nome convenzione Consip |
| `lotto` | VARCHAR | Lotto della convenzione |
| `valore_economico_consumi` | DOUBLE | Valore economico consumi (€) |
| `numero_ordini_con_consumi` | BIGINT | Numero ordini con consumi |
| `n_pa_con_consumi` | BIGINT | Numero PA con consumi |
| `n_po_con_consumi` | BIGINT | Numero punti di prelievo con consumi |

## Rischi noti

- **Sede fornitore ≠ luogo esecuzione**: la regione del fornitore non coincide necessariamente con il luogo dove il servizio viene erogato
- **Non copre tutte le categorie merceologiche Consip**: solo utility (energia, gas, carburanti)
- **Serie storica breve**: 3 anni (2023-2025), insufficiente per trend strutturali
- **Dati aggregati, non additivi**: i valori sono aggregate statistiche, non transazioni singole
- **File 2026 identico a 2025**: il file nominato 2026 è copia del 2025 (dato non ancora aggiornato). Anni validi: 2023-2025.

## Stato

- intake

## Prossimo passo

Run pipeline: `toolkit run all --config candidates/consip-consumi-convenzione/dataset.yml --years 2025`
