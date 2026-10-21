# richiedenti-asilo-italia

**Domande e decisioni di protezione internazionale in Italia (2008-2025)** — Eurostat
(`MIGR_ASYAPPCTZA` domande, `MIGR_ASYDCFSTA` decisioni).

Issue intake: #597

## Domanda civica

Quante persone chiedono asilo in Italia ogni anno e quante ottengono davvero una
protezione? Per nazionalità, il tasso di riconoscimento è cambiato nel tempo? E quanto
pesa la domanda reiterata?

La tensione: il dibattito pubblico misura l'asilo in "arrivi" e "dinieghi", ma il dato
che conta per chi chiede protezione è il tasso di esito per paese di origine — che varia
di oltre 10 volte tra nazionalità.

## Dataset / fonte

- **Fonte**: Eurostat — `migr_asyappctza` (domande di protezione internazionale) e
  `migr_asydcfsta` (decisioni di primo grado), filtro `geo=IT`.
- **Perché non la CNA**: il portale open data della Commissione Nazionale per il Diritto
  d'Asilo (`asylum-opendata.dlci.interno.it`, brand `dati.cna.it`) è dismesso: risponde
  200 con un body placeholder di 11 byte, tutti i path noti sono 404, il dominio
  `dati.cna.it` non risolve e non esistono copie dei CSV nell'archivio web. Dettagli in
  `notes.md`.
- **Copertura**: 2008-2025, 201 cittadinanze, 3.618 righe nel mart annuale.
- **Schema**: `anno`, `cittadinanza_codice` (ISO2), `cittadinanza`, `domande`,
  `domande_prima_istanza`, `domande_reiterate`, `reiterate_derivate`, `decisioni`,
  `accolte`, `rifugiati`, `protezione_sussidiaria`, `protezione_umanitaria`, `dinieghi`,
  `tasso_riconoscimento`, `tasso_diniego`, `quota_reiterate`.
- **Mart**: `mart_asilo_annuale` (anno × cittadinanza), `mart_asilo_italia` (serie
  nazionale).
- **Riconciliazione**: `mart_asilo_italia` usa la riga Eurostat `TOTAL`, che include
  anche `UNK` (cittadinanza ignota) e l'arrotondamento a 5. `mart_asilo_annuale` esclude
  gli aggregati, quindi la somma per cittadinanza non coincide col totale nazionale:
  usare `mart_asilo_italia` per i totali e `mart_asilo_annuale` per i confronti tra paesi.

## Perché vale la pena

- Unico dato strutturato, aggiornato e scaricabile su domande + esiti per nazionalità.
- Risponde alla domanda civica senza dipendere da PDF: i riepiloghi CNA sono solo
  aggregati nazionali, non hanno tabelle per Commissione Territoriale.
- Incrociabile con `sbarchi-migranti-italia` e `centri-accoglienza-italia` (stessa
  categoria).

## Output minimo atteso

Clean parquet + due mart. Numeri chiave: 158.605 domande nel 2024 (picco serie),
104.560 decisioni nel 2025 con tasso di riconoscimento 30,0%; nel 2024 il tasso è 35,9%
(Bangladesh 19,7%, Burkina Faso 98,8%), in calo dal 48,4% del 2022.

## Criterio di promozione

- Run stabile e riproducibile (script source, nessun file dati committato).
- Serie 2008-2025 completa lato domande e decisioni.
- Nota metodologica esplicita su: arrotondamento Eurostat a 5, etichette cittadinanza in
  inglese, scarto tra `NEG` Eurostat e "dinieghi" CNA, reiterate derivate 2008-2020
  (`reiterate_derivate`) perché `SSEQ` è pubblicato solo dal 2021 (vedi `notes.md`).

## Stato

- [x] scaffold + run raw/clean/mart (validate ok, 30.454 righe clean)
- [x] confronto con riepilogo ufficiale CNA 2022
- [x] audit dati + hardening script (reiterate derivate, cast BIGINT, retry/fail-fast,
      dedupe, scrittura atomica, sanity check)
- [ ] PR + review
