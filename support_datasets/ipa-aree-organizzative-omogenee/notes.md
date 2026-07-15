# ipa-aree-organizzative-omogenee — note tecniche

## Formato

Il dataset IPA AOO è distribuito come file XLSX (~6 MB, unico foglio "Sheet1").
Il toolkit lo legge nativamente tramite `pandas.read_excel()` con engine `openpyxl`.

## Clean

- Tutte le colonne sono CAST a VARCHAR + trim per robustezza
- Righe con `codice_uni_aoo` nullo o vuoto vengono escluse

## Validazione

- clean: min_rows=30000 (attese ~39380)
- mart: pass-through, min_rows=30000

## Cross-reference

- `codice_ipa` → join con `ipa_enti` e `bdap_anagrafe_enti`
- `codice_uni_aoo` → join con `ipa_unita_organizzative`
