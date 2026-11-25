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

## I codici: anagrafica giusta, non crosswalk mancante

- La matrice 2021 usa i codici provinciali sardi **090/091/092/095/111**; l'elenco comuni
  2026 usa i **nuovi 112-119** (riforma 2025). Un join sull'elenco perdeva 394 comuni.
- **`comuni_master` conserva la generazione 2021** e copre 7.887 comuni su 7.904 (99,8%):
  è l'anagrafica corretta da usare come support.
- Restano **17 comuni** (fusioni recenti, 7 province: 005, 012, 013, 018, 024, 025, 028)
  senza corrispondenza, per 9.917 uscenti (0,1%). Il mart li tiene con nome `NULL` e
  `in_anagrafica = false`.
- Lezione: quando un join perde un'intera area, il sospetto va prima sull'**anagrafica**
  (vintage dei codici), non sui dati. Il crosswalk esisteva già, in un altro dataset.

## Metodo: è una stima, non un conteggio

- ISTAT **non conta** i pendolari: stima i flussi con un modello che integra il censimento
  2021 (campione) con Registro Base degli Individui, INPS, Certificazione Unica/Anagrafe
  Tributaria e una matrice di distanze (nota metodologica 2/10/2025, agg. 3/11/2025).
  L'approccio predittivo sostituisce il conteggio pieno usato nel 2011.
- Definizione: occupato che si reca **almeno 3 giorni a settimana** al lavoro, partendo
  dall'alloggio e rientrando ogni giorno. Esclusi chi lavora da casa e chi non ha sede fissa.
- I flussi sotto soglia di riservatezza non sono pubblicati: **assenza di coppia ≠ zero
  pendolari**.
- 19.565.808 pendolari corrispondono a circa l'83% degli occupati (focus ISTAT sui Sistemi
  Locali del Lavoro 2021, derivati da questa stessa matrice).

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
