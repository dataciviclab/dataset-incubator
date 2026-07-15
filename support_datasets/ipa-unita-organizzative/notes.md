# ipa-unita-organizzative — note tecniche

## Formato

Il dataset IPA UO è distribuito come file XLSX (~15 MB, unico foglio "Sheet1").
Il toolkit lo legge nativamente tramite `pandas.read_excel()` con engine `openpyxl`.

## Clean

- Tutte le colonne sono CAST a VARCHAR + trim per robustezza
- Le colonne `Mail4`, `Mail5`, `Tipo_Mail4`, `Tipo_Mail5` sono assenti dal file XLSX
  (presenti invece nel dataset `ipa_enti` come CSV)
- Righe con `codice_uni_uo` nullo o vuoto vengono escluse

## Gerarchia

Il campo `codice_uni_uo_padre` permette di ricostruire l'albero organizzativo.
Esempio di CTE ricorsiva per un ente specifico:

```sql
WITH RECURSIVE tree AS (
  SELECT codice_uni_uo, descrizione_uo, codice_uni_uo_padre, 1 AS livello
  FROM clean_input
  WHERE codice_ipa = 'm_dg' AND codice_uni_uo_padre IS NULL
  UNION ALL
  SELECT uo.codice_uni_uo, uo.descrizione_uo, uo.codice_uni_uo_padre, tree.livello + 1
  FROM clean_input uo
  JOIN tree ON uo.codice_uni_uo_padre = tree.codice_uni_uo
)
SELECT * FROM tree ORDER BY livello, descrizione_uo;
```

## Validazione

- clean: min_rows=100000 (attese ~122470)
- mart: pass-through, min_rows=100000

## Cross-reference

- `codice_ipa` → join con `ipa_enti` e `bdap_anagrafe_enti`
- `codice_uni_aoo` → join con `ipa_aree_organizzative_omogenee`
