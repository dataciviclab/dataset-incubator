# ANAC — Subappalti (support)

**Dataset**: `anac_subappalti`
**Tipo**: support — subappalti e filiera esecutiva
**Fonte**: ANAC — Autorità Nazionale Anticorruzione
**Protocollo**: CKAN (via dati.gov.it)
**Licenza**: CC BY 4.0

## Contenuto

Autorizzazioni al subappalto comunicate all'ANAC. Colma il gap tra `flag_subappalto` (che dice solo SE c'è subappalto) e l'effettiva filiera: chi subappalta a chi, per quali lavori, in quali categorie.

## Schema (15 colonne)

| Colonna | Tipo | Descrizione |
|---|---|---|
| `cig` | VARCHAR | CIG del contratto principale |
| `id_subappalto` | VARCHAR | ID univoco subappalto |
| `cf_subappaltante` | VARCHAR | CF dell'aggiudicatario che subappalta |
| `data_autorizzazione` | DATE | Data autorizzazione |
| `oggetto` | VARCHAR | Oggetto del subappalto |
| `cod_categoria` | VARCHAR | Categoria lavori |
| `cod_cpv` | VARCHAR | CPV del subappalto |
| `codice_fiscale` | VARCHAR | CF del subappaltatore |
| `denominazione` | VARCHAR | Ragione sociale subappaltatore |
| `tipo_soggetto` | VARCHAR | Tipo soggetto |

## Join chain

- `subappalti (cig)` → `anac_bandi_gara (cig)` / `anac_aggiudicazioni (cig)`
- `subappalti (cf_subappaltante)` → `anac_aggiudicatari (codice_fiscale)` — SA subappaltanti
- `subappalti (codice_fiscale)` → `anac_aggiudicatari (codice_fiscale)` — subappaltatori che vincono anche gare dirette

## Limiti

- Copertura parziale: solo gare dove il subappalto è stato dichiarato e autorizzato
- `cf_subappaltante` spesso nullo
- Frequenza annuale
