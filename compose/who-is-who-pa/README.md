# who-is-who-pa

Compose del filone **struttura della PA**. Unisce 3 support dataset in un'unica vista: per ogni unità organizzativa (UO), il contesto dell'ente, il responsabile, i contatti e l'area organizzativa.

## Domanda

Chi è il responsabile di un ufficio specifico nella PA? Quali sono i suoi contatti (email, PEC, telefono)? A che area organizzativa appartiene? Qual è il vertice dell'ente?

## Fonti

| ID | Dataset | Fonte | Output |
|---|---|---|---|
| Enti | `support_datasets/ipa-enti` | AgID — IndicePA | Anagrafica enti, categorie, vertici |
| UO | `support_datasets/ipa-unita-organizzative` | AgID — IndicePA | Uffici, gerarchia, responsabili, contatti |
| AOO | `support_datasets/ipa-aree-organizzative-omogenee` | AgID — IndicePA | Aree organizzative, protocollo |

## Output

Singolo mart `who_is_who_pa` con **122.470 righe** e **36 colonne**:

| Blocco | Colonne principali |
|---|---|
| **Ente** | codice_ipa, denominazione_ente, codice_categoria, tipologia, acronimo |
| **Vertice ente** | vertice_ente_titolo, vertice_ente_nome, vertice_ente_cognome |
| **Unità organizzativa** | codice_uni_uo, descrizione_uo, codice_uni_uo_padre |
| **Responsabile UO** | uo_resp_nome, uo_resp_cognome, uo_resp_email, uo_resp_telefono |
| **Contatti UO** | uo_mail, uo_tipo_mail (Pec/Altro), uo_mail2 |
| **Area organizzativa** | denominazione_aoo, aoo_resp_nome, aoo_mail, protocollo_informatico |
| **Sede** | codice_comune_istat, cap, indirizzo |

## Esempio

```sql
SELECT denominazione_ente, descrizione_uo,
       uo_resp_nome, uo_resp_cognome, uo_resp_email, uo_mail, uo_tipo_mail
FROM who_is_who_pa
WHERE denominazione_ente = 'Comune di Abbiategrasso'
ORDER BY descrizione_uo;
```

Risultato: 7 uffici del comune, con responsabile (nome+cognome), email diretta e PEC istituzionale.

## Esecuzione

```bash
toolkit run full --config compose/who-is-who-pa/dataset.yml
```

I parquet upstream sono letti direttamente da GCS via DuckDB `read_parquet()` — nessuna estensione httpfs necessaria.

## Join graph

```
ipa_enti ──codice_ipa──┐
                        ├──→ who_is_who_pa
ipa_unita_org. ────────┘
       │
       └──codice_uni_aoo──→ ipa_aree_organizzative_omogenee
```
