# BDAP Pagamenti Stato — Consuntivo

**Pagamenti del Bilancio dello Stato per Amministrazione, Missione e Categoria Economica.**

Il **consuntivo** dei pagamenti dello Stato: quanto lo Stato ha *realmente pagato*
ogni anno, per ministero, missione e categoria economica. Complementare a
`bdap_spese_stato` (previsioni), è il dato **reale** di cassa.

- **Copertura:** 2014-2025 (consuntivi annuali)
- **Granularità:** Amministrazione × Missione × Categoria economica × anno
- **Fonte:** MEF / OpenBDAP (CKAN)
- **Unità:** euro

## Cosa permette

- Il costo **consuntivo** del debito pubblico (missione "Debito pubblico",
  categorie interessi e rimborso)
- La quota del bilancio assorbita da ogni missione, con dati pagati reali
- Confronto previsione (bdap_spese_stato) vs consuntivo (questo dataset)

## Esempio (missione Debito pubblico, consuntivo 2024)

| Categoria | Importo |
|---|---|
| INTERESSI PASSIVI E ALTRI ONERI FINANZIARI | 82,1 mld |
| RIMBORSO PASSIVITA' FINANZIARIE | 282,6 mld |
| ACQUISIZIONI DI ATTIVITA' FINANZIARIE | 3,0 mld |
| CONSUMI INTERMEDI | 0,9 mld |

## Struttura

16 colonne: 7 dimensioni (anno, ministero, amministrazione, missione, categoria)
+ 9 metriche per canale di pagamento (Erario, Tesoreria, Esterno, Note
Imputazione...) incluso il totale.

## Trasparenza e limiti

- Consuntivi annuali (dati osservati l'anno successivo)
- Gli importi per categoria non sono disaggregati per singola operazione
- Il servizio del debito transita in larga parte da "Note di imputazione"
