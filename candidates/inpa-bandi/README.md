# inpa-bandi

**Bandi e avvisi nel Portale inPA** (Portale unico del Reclutamento della PA).

Snapshot dei bandi pubblicati su https://www.inpa.gov.it/ — la piattaforma
istituzionale obbligatoria per concorsi, avvisi di mobilità e selezioni della
Pubblica Amministrazione. Copre OPEN (con dettaglio) e storico CLOSED.

- **Fonte**: API pubblica non documentata `https://portale.inpa.gov.it/concorsi-smart/api/concorso-public-area/search-better`
- **Licenza**: dati pubblici PA (D.Lgs. 33/2013)
- **Copertura**: snapshot vivo (2026), archivio completo dal 2022 (~73.000 bandi)
- **Granularità**: singolo bando/avviso con posti, ente, sedi, scadenze, tipo procedura

## Domanda civica

Dove sono e come funzionano i concorsi pubblici in Italia? Quali enti assumono di più,
in quali aree, con quali profili e quali scadenze? Il reclutamento PA è trasparente e
accessibile?

## Shape

- ~73.000 bandi (2.256 OPEN + 71.000 CLOSED, snapshot 2026-08)
- Campi: id, codice, titolo, figura_ricercata, data_pubblicazione, data_scadenza,
  num_posti, tipo_procedura, categoria, settore, regione, provincia, ente, status
- OPEN arricchiti dal dettaglio: company_district_code, link_sito_pa, n_allegati, is_remote
- Cross-link: `concorso_id` collega bando ↔ comunicazioni di procedura (calendari, graduatorie)

## Perché vale la pena

- Unica fonte istituzionale strutturata sul reclutamento PA (dal 2023 obbligatoria per tutti gli enti)
- Serie storica 2022-2026: trend di bandi, posti, enti per anno
- Incrociabile con `open-conto-annuale` (personale) e `inpa-comunicazioni` (esiti)

## Output minimo atteso

- Dataset clean interrogabile via SQL con bandi per regione, ente, categoria, scadenza, anno
- Mart sintesi/trend per rispondere a domande su dove/quanto si recluta in PA

## Stato / prossimo passo

- [ ] Harvest del dettaglio anche su CLOSED (volume alto, ~7h — rimandato)
- [ ] Mart enti locali per regione (reclutamento vs organico, join conto annuale)
