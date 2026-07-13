# Note tecniche — mur_immatricolati

## Portale CKAN

- URL base API: `https://dati-ustat.mur.gov.it/api/3/action`
- Redirect HTTP → HTTPS
- Dataset contiene 20 risorse (CSV + 1 XLSX informativo)
- Encoding: latin-1 (ISO-8859-1)

## Perimetro v0

Risorse selezionate:
- **ateneo**: immatricolati per ateneo, sesso (4.811 righe, 28 anni × ~86 atenei × 2 sessi)
- **gruppo**: immatricolati per gruppo disciplinare, sesso (840 righe)
- **classe**: immatricolati per classe di laurea, sesso (3.233 righe)

## Estensioni future

- Aggiungere risorse per: anno di nascita, residenza, tipo diploma, voto
- Aggiungere risorse internazionali (paese, ateneo, classe)
- Arricchire atenei con regione/provincia (da COD ateneo → lookup MUR)
