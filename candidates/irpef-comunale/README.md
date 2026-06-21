# irpef-comunale

**Domanda principale:** Come varia la capacità fiscale tra comuni e regioni italiane?

Redditi IRPEF dichiarati da persone fisiche, per comune italiano. Include
numero contribuenti, imponibile, imposta netta, addizionali e distribuzione
per fasce di reddito.

---

## Fonte

MEF — Dipartimento delle Finanze. ZIP annuali pubblicati su:
```
https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/
Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_{year}.zip
```

Anni disponibili dalla fonte: **2000–2024** (URL pattern confermato).
Attualmente intakati: **2019–2024** (6 anni).

## Schema clean (52 colonne)

| Col | Nome | Note |
|:---:|------|------|
| 0 | `anno_di_imposta` | |
| 1 | `codice_catastale` | Chiave di join con `comuni_master` |
| 2 | `codice_istat_comune` | Chiave di join con `comuni_master` |
| 3–6 | Anagrafica comune | denominazione, provincia, regione |
| 7 | `numero_contribuenti` | Totale contribuenti del comune |
| 8–9 | Reddito da fabbricati | frequenza + ammontare |
| 10–11 | Reddito lav. dipendente | frequenza + ammontare |
| 12–13 | Reddito da pensione | frequenza + ammontare |
| 14–21 | Altri redditi | autonomo, impresa, partecipazione |
| 22–23 | `reddito_imponibile` | **freq + eur** — copertura 2019–2024 |
| 24–25 | `imposta_netta` | **freq + eur** — copertura 2019–2024 |
| 26–27 | Bonus / Trattamento | semantica varia per anno (vedi caveat) |
| 28–31 | Addizionali | regionale + comunale |
| 32–33 | Addizionale comunale | freq + eur |
| 34–35 | `reddito_complessivo` | **freq + eur** — solo 2023+ |
| 36–51 | Fasce reddito complessivo | 8 fasce × (freq + eur) |

## Copertura

| Dimensione | Valore |
|------------|--------|
| **Anni** | 2019–2024 (6 anni) |
| **Territorio** | ~7.900 comuni/anno |
| **Variabili** | 52 colonne (26 metriche × freq/eur) |
| **Contribuenti (Italia, 2024)** | ~41,6M |

## Join con altri dataset

Tramite `codice_istat_comune` (6 cifre) si collega a `comuni_master` e quindi
a tutti i dataset del Join Map Registry (`registry/join_map.yaml`).

Usato in `candidates/unified-comuni/` per la colonna `reddito_imponibile_eur`
(copertura 2019–2024) e `reddito_procapite` (calcolato su popolazione ISTAT).

## Mart disponibili

| Mart | Descrizione |
|------|-------------|
| `irpef_by_regione` | Aggregazione per regione |
| `irpef_by_comune` | Vista per comune con indicatori |
| `irpef_capacita_fiscale_multi_anno` | Serie storica con rank nazionale/regionale e delta YoY |

## Limiti

- **`reddito_complessivo_eur`** popolato solo dal 2023. Per 2019–2022 usare `reddito_imponibile_eur`.
- **Bonus vs Trattamento** (col 26–27): il MEF ha cambiato semantica nel 2021. Non confrontabili direttamente.
- **Somalettura regionale**: la somma dei comuni può non coincidere con i totali regionali ufficiali.

## Note tecniche

Vedi `notes.md` per dettagli su struttura raw, schema, e caveat operativi.

Il layer pubblico (notebook, analisi) vive in `dataciviclab/analisi/irpef-comunale/`.
