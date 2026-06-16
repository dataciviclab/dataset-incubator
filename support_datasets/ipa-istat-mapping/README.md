# IPA ↔ ISTAT mapping — comuni italiani

## Dataset

Tabella di raccordo tra **IPA** (Indice delle Pubbliche Amministrazioni, AgID) e **ISTAT** (codici amministrativi). Una riga per comune italiano con codice ISTAT, codice IPA, codice fiscale, codice catastale e dati anagrafici/territoriali.

- **fonte 1**: IPA enti — [datastore AgID](https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True)
- **fonte 2**: ISTAT comuni — [Elenco codici unità amministrative](https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv)
- **perimetro**: soli comuni (categoria IPA `L6`)
- **copertura**: **7.412 / 7.415 comuni (99,96%)** — Sardegna inclusa
- **snapshot**: 2026

## Perché vale la pena averlo

È un **support dataset ad alto impatto cross-analisi**. Serve per:

- **Join tra dataset IPA e ISTAT** — molti dataset Lab usano codici ISTAT (6 cifre), molti dataset PA usano codici IPA (es. MEF partecipazioni, BDAP)
- **Arricchimento anagrafico** — da IPA si ottiene codice fiscale, indirizzo PEC, sito istituzionale per ogni comune
- **Chiave di raccordo** — il codice fiscale dell'ente permette join con BDAP, MEF e altri dataset finanziari

## Output

### `mart_ipa_istat`
16 colonne — una riga per comune:

| Colonna | Descrizione |
|---|---|
| `codice_istat` | Codice ISTAT 6 cifre |
| `denominazione` | Nome comune (ISTAT) |
| `regione` | Regione |
| `sigla_provincia` | Sigla provincia |
| `codice_regione` | Codice regione ISTAT (2 cifre) |
| `codice_catastale_istat` | Codice catastale (Belfiore, da ISTAT) |
| `codice_ipa` | Codice IPA (es. `c_b354`) |
| `codice_fiscale` | Codice fiscale ente |
| `denominazione_ipa` | Denominazione ente in IPA |
| `codice_categoria` | Categoria IPA (sempre `L6`) |
| `codice_catastale_comune` | Codice catastale (da IPA) |
| `codice_istat_ipa` | Codice ISTAT attribuito da IPA |
| `acronimo` | Acronimo (se presente) |
| `indirizzo` | Indirizzo sede |
| `cap` | CAP |
| `sito_istituzionale` | Sito web |

## Note tecniche

- La chiave di join è il **codice catastale (Belfiore)**, non il codice ISTAT: IPA usa un sistema di codifica proprio per `Codice_comune_ISTAT` che non coincide con i codici ISTAT per tutte le regioni (es. Sardegna)
- **3 comuni senza match IPA**: verosimilmente comuni cessati o fusi — da verificare
- IPA filtrato per sola categoria `L6` (Comuni). Per altri enti (province, ASL, università) serve un'estensione
