# Note tecniche — pnrr-gare

## Fonte

**Italia Domani** (MEF / SoGeI), fonte dati ReGiS.
- Landing page: https://www.italiadomani.gov.it/content/sogei-ng/it/it/catalogo-open-data.html
- URL diretto CSV: https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Gare.csv
- Licenza: da verificare (dati pubblici — stessa fonte di pnrr-progetti)

## Download (AEM/Akamai)

Il server AEM/Akamai blocca python-requests ma **accetta wget** (pattern
verificato in CI).
- `preprocess.py`: wget con User-Agent "Mozilla/5.0 (X11; Linux x86_64)
  AppleWebKit/537.36", fallback su urllib se wget non disponibile.
- Dataset.yml con `type: script`.
- Per CI: `TOOLKIT_ALLOW_SCRIPT_SOURCE=1` (guardrail, come pnrr-progetti).

## Formato

- CSV delim `;`, encoding UTF-8 con BOM (`utf-8-sig`)
- Importi in formato italiano (virgola decimale) → `clean.read.decimal: ","`
- Date `DD/MM/YYYY` → `TRY_STRPTIME(..., '%d/%m/%Y')` in clean.sql

## Deroga primary_key (clean)

Nessuna chiave naturale unica:
- 25.250 righe (8,9%) senza CIG (assenza per legge — campi
  `Codice Motivo Assenza CIG` / `Descrizione Motivo Assenza CIG`)
- 1.057 coppie `(cig, cup)` duplicate (una stessa coppia con importi diversi,
  probabile multi-lotto/più righe per gara)
- La chiave più vicina è `(cig, cup, codice_interno_pda)` ma non garantita unica

Deroga documentata, non è dichiarato `clean.validate.primary_key`.
`not_null` solo su `cup` (presente al 100%). `importo_complessivo_gara`/`importo_aggiudicazione`
non sono not_null: 99 righe (0,03%) li hanno NULL (record parziali legittimi del source).

## Confronto con ANAC (2026-08-05)

PNRR_Gare NON è ridondante rispetto ad ANAC (master, 6,08M CIG):
- 67% dei CIG PNRR_Gare è presente in ANAC; di questi 83% ha `flag_pnrr=true`
- ANAC conta 341.121 CIG `flag_pnrr=true`, ma solo 40% compaiono in PNRR_Gare
  (i restanti includono PNC e dichiarazioni non allineate a ReGiS)
- Join consigliato via **CUP** (63.499 unici) → `anac_cup`, non via CIG 1:1

## Riferimenti

- Issue intake: #517
- Dataset complementari: `pnrr_progetti` (candidate), `anac_appalti_master` (pubblicato)
