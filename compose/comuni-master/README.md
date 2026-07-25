# Comuni Master — raccordo completo comuni italiani

## Dataset

Dataset composito che fonde 3 fonti: `istat-elenco-comuni` (ISTAT SITUAS), ISTAT CSV (codici NUTS, ripartizione, codici storici) e `ipa-enti` (AgID IPA). Una riga per comune italiano, 38 colonne.

- **fonte 1**: `istat-elenco-comuni` (GCS) — codici ISTAT, catastali, superficie, popolazione, altitudine
- **fonte 2**: ISTAT CSV (raw) — NUTS 2021/2024, ripartizione geografica, flag capoluogo, codici storici 103/107/110
- **fonte 3**: `ipa-enti` (GCS, L6) — codici IPA, fiscale, contatti
- **copertura**: 7.894 comuni, 38 colonne
- **NUTS3**: 7.768 (98,4%)
- **IPA**: 7.893 (99,99%)
- **snapshot**: 2026

## Output

### Clean (38 colonne, su GCS)

Anagrafica: `codice_istat`, `denominazione`, `codice_catastale`, `sigla_provincia`, `provincia`, `regione`

Territorio: `superficie_km2`, `popolazione_residente`, `popolazione_legale`, `zona_altimetrica`, `altitudine`, `comune_litoraneo`, `comune_isolano`

NUTS: `nuts1_2021`, `nuts2_2021`, `nuts3_2021`, `nuts1_2024`, `nuts2_2024`, `nuts3_2024`

Classificazione: `codice_ripartizione`, `ripartizione`, `flag_capoluogo`, `codice_tipologia_uts`, `denominazione_uts`, `denominazione_altra_lingua`

Codici storici: `codice_110_province`, `codice_107_province`, `codice_103_province`

IPA: `codice_ipa`, `codice_fiscale`, `denominazione_ipa`, `codice_categoria`, `codice_catastale_comune`, `codice_istat_ipa`, `acronimo`, `indirizzo`, `cap`, `sito_istituzionale`

### Mart (pass-through, stesse colonne del clean)

## Perché vale la pena averlo

Unico punto di verità per i comuni italiani in tutto il Lab. Sostituisce `ipa-istat-mapping` e fornisce NUTS e codici storici per mapping cross-anno e join con dati Eurostat.
