# Notes

## Tecnico

- I due file hanno **lo stesso tracciato con suffisso diverso** (`Procom_lav` vs `Procom_stu`).
  Con `clean.read.mode: all` e `union_by_name` il view `raw_input` espone entrambe le coppie
  di colonne, una nulla per file: il discriminante è quale `Procom_*` è valorizzato. Se il
  toolkit smettesse di usare `union_by_name`, il clean produrrebbe una sola matrice senza
  errore — il controllo `min_rows: 600000` è la sentinella contro questo caso.
- `unzip_first` (non `unzip_first_csv`): dentro gli ZIP c'è un `.txt`, non un `.csv`.
- `delim: "\t"`, CRLF, header presente; `all_varchar: true` perché i codici hanno zeri
  iniziali (`001001`).
- `warn_removed_columns: false`: il clean rinomina esplicitamente tutte le colonne.

## Il problema dei codici (da risolvere prima della promozione)

- **394 comuni di origine** della matrice 2021 non esistono nell'anagrafica 2026
  (`istat_elenco_comuni`): 377 sardi (prefissi 090/091/092/095/111), il resto fusioni.
- Il mart li mantiene, con `in_anagrafica_2026 = false` e nome `NULL`, e vale 216.023
  uscenti (2,2%).
- **Non usare un inner join sull'anagrafica**: sparirebbero 394 comuni, inclusa Sassari.
  Il primo caso è 092051 → 092009 con 9.501 pendolari, sesto flusso nazionale.
- Serve un crosswalk 2021 → 2026. Non esiste in casa: va costruito da ISTAT "variazioni
  territoriali" o mappato a mano (377 codici sardi, una volta).

## Analitico

- **Definizioni**: `uscenti` = residenti che lavorano/studiano in un altro comune; `entranti`
  = non residenti che vengono nel comune; `intra` = spostamenti dentro il comune di
  residenza. `lavoro_auto_contenimento_pct = intra / (intra + uscenti)`: 100% = nessuno esce.
- **Attenzione ai valori assoluti**: i comuni con più uscenti sono le grandi città (Milano
  98.017), perché la graduatoria è in valore assoluto. Il tasso di uscita per 100 residenti è
  più informativo sui dormitori, ma usa la popolazione totale (non gli occupati): è un
  indicatore grezzo, da etichettare come tale.
- Il saldo entranti-uscenti non è un indicatore di benessere: un polo con saldo positivo può
  avere anche un'elevata uscita (Milano: 98.017 uscenti).
- **Studio e lavoro non si sommano**: destinazioni e bacini diversi (università vs poli
  produttivi). Tenuti separati nei mart.

## Cautele

- **Una sola edizione**: la matrice esce con l'edizione censuaria, non ogni anno. Nessuna
  serie storica: 2011 e 2021 sono disponibili, con codici e perimetri diversi.
- Il file contiene solo coppie con almeno un pendolare: i comuni senza flussi non compaiono,
  e un'assenza non significa "zero pendolari" ma "sotto la soglia di pubblicazione".
- I codici sono quelli del 2021: non usarli per join su anagrafiche successive senza
  crosswalk (vedi sopra).
- I totali nazionali del mart (`sum(lavoro_intra)` + `sum(lavoro_uscenti)`) sono il controllo
  di coerenza: 9.803.786 + 9.762.022 = 19.565.808.
