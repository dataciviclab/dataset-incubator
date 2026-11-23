# Notes

## Tecnico

- `clean.read.all_varchar: true` obbligatorio: `CodiceIstat` ha zeri iniziali (`028001`) e
  `ComuneID` e' un codice catastale (`A001`).
- **`Descrizione` = nome del comune**, non descrizione dell'intervento. Verificato sulle
  prime righe (`A001` -> "Abano Terme").
- **`-1` come sentinella**: 48 interventi su `AlloggiAssegnatiNumero`, 1 su
  `AlloggiSfrattoNumero`. Convertito in `NULL` in clean; sommarlo falsa il totale (6.569
  invece di 6.521 se lo si somma come -1, 6.617 se lo si tratta come zero).
- **5 interventi con date invertite** (fine lavori precedente all'inizio): Aulla, Certaldo,
  Finale Emilia, Novara, Trieste. La durata resta `NULL` e la riga e' marcata con
  `date_incoerenti`, invece di produrre una durata negativa o di scartare il record.
- `max_null_pct` dichiara i null attesi (date mancanti ~35-42%): una regressione della fonte
  che li fa salire oltre soglia rompe il run.
- Il dataset non ha un campo "anno": `annualita_programma` e' un intervallo testuale
  (`2014-2017`, `2014-2024`) e `periodo_monitoraggio` e' la data dello snapshot di
  monitoraggio (2016-10 -> 2020-04).

- **La fonte e' ferma.** `Last-Modified` del CSV: 2022-03-04; ultimo `PeriodoMonitoraggio`:
  2020-04-01; ultima `LavoriUltimatiData`: 2020-03-06. Il campo `Annualita` ("2014-2024") e'
  l'etichetta del programma e non la fine dei dati: leggerlo come copertura e' l'errore
  naturale su questo tracciato. Il catalogo MIT dichiara aggiornamento ogni 6 ore, ma
  `metadata_modified` della scheda e' 2022-03-04 come il file.
- Contesto del catalogo: su 71 dataset pubblicati su `dati.mit.gov.it`, **60 hanno
  `metadata_modified` nel 2022**; solo 5 risultano aggiornati nel 2026. Non e' un caso
  isolato, e' lo stato del catalogo.

## Analitico

- La catena e' **finanziato -> alloggi previsti -> date lavori -> assegnati**. "Assegnati" e'
  un campo dichiarato, non verificato: 643 interventi "Completato" hanno 0 assegnati e il
  dataset non distingue "non ancora assegnati" da "non comunicato".
- Per questo la quota di assegnazione e' un **limite inferiore** dell'efficacia, non una
  misura. Il README lo dichiara e il mart non deve essere presentato come "solo 1 su 4".
- **Il campo non regge il confronto territoriale.** In Veneto il 96% degli interventi
  completati ha 0 assegnati (27 su 28), in Sardegna l'80%, in Sicilia il 69%, contro l'11%
  della Liguria: e' pratica di comunicazione, non allocazione. Un ranking regionale basato su
  `quota_assegnati_pct` e' un artefatto e non va pubblicato.
- La quota dipende dalla **dimensione**: 49,8% sugli interventi da 1 alloggio, 17,8% su quelli
  da 21+ (A1 65,6% vs B1 15,0%). Il 24,9% nazionale e' la media di due regimi diversi.
- **I fallimenti sono micro**: 646 dei 692 "non piu' realizzabile" sono interventi da 1 alloggio.
- **Un errore nei dati**: `080347 Cattolica` ha 3 alloggi previsti e 6 assegnati (unico su 5.560).
- 692 interventi "non piu' realizzabile" su 5.560 (12,4%) sono una quota di fallimento
  dichiarata dalla fonte: e' un dato raro e va usato cosi'.
- La durata mediana (43 giorni sul "Completato") e' la differenza tra due date dichiarate:
  non e' un tempo di cantiere verificato.

## Cautele

- Copre **un solo programma** (DL 47/2014, ~451 mln). Il PINQuA (PNC, ~2,8 mld) non e'
  incluso e non e' isolabile ne' in OpenCUP (36 progetti per `descrizione_intervento`) ne' in
  OpenCoesione (0 progetti).
- Nessun dato sullo **stock** ERP: Federcasa 2024/25 stima 797.034 alloggi (report PDF). Senza
  stock, "assegnati su previsti" non dice la copertura rispetto al bisogno.
- Manca il Trentino-Alto Adige: le province autonome non partecipano al programma.
- `alloggi_previsti` e' il numero dichiarato dall'attuatore all'ammissione, non un collaudo.
- Nessuna causalita': un comune con quota bassa non e' necessariamente inefficiente, puo'
  semplicemente aver comunicato meno.
