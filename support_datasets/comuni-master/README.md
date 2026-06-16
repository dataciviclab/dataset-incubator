# Comuni Master — raccordo completo comuni italiani

## Dataset

Support dataset che fonde `istat-elenco-comuni` (ISTAT SITUAS) e `ipa-istat-mapping` (IPA AgID) in un'unica tabella. Una riga per comune italiano con tutte le codifiche (ISTAT, catastale, IPA, fiscale) e i dati territoriali (superficie, popolazione, altitudine, ecc.).

- **fonte 1**: ISTAT Elenco Comuni — codici ISTAT, catastali, superficie, popolazione, altitudine
- **fonte 2**: IPA↔ISTAT mapping — codici IPA, fiscale, indirizzo, PEC, sito
- **copertura**: 7.894 comuni, 24 colonne
- **snapshot**: 2026

## Output

### Clean (24 colonne, su GCS)

`codice_istat`, `denominazione`, `codice_catastale`, `sigla_provincia`, `provincia`, `regione`, `superficie_km2`, `popolazione_residente`, `popolazione_legale`, `zona_altimetrica`, `altitudine`, `comune_litoraneo`, `comune_isolano`, `codice_ipa`, `codice_fiscale`, `codice_categoria`, `codice_catastale_comune`, `codice_regione`, `codice_istat_ipa`, `denominazione_ipa`, `acronimo`, `indirizzo`, `cap`, `sito_istituzionale`

### Mart (pass-through, stesse colonne del clean)

## Perché vale la pena averlo

Unico punto di verità per i comuni italiani in tutto il Lab. Sostituisce la necessità di fare JOIN tra due support dataset separati.
