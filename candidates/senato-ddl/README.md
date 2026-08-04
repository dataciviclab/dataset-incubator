# senato-ddl

**Domanda guida:** Come nasce e muore una legge in Senato? Iter completo di un disegno di legge: presentazione, stato, tempi, fasi.

**Fonte:** Senato della Repubblica — OpenData SPARQL (`https://dati.senato.it/sparql`)
**Dataset:** graph `ddl/19` (XIX legislatura), classe `osr:idDdl`
**Licenza:** CC BY 3.0

## Perché vale la pena

Complementare a `italia-corpus` (Normattiva = leggi vigenti): questo dà l'**iter parlamentare** dal deposito all'approvazione. Ddl mai approvati, tempi per stato, produttività legislativa — il cuore del processo legislativo, oggi assente nel Lab (issue #781).

## Output minimo atteso

- `mart_stato`: ddl per stato dell'iter (approvati vs fermi)
- `mart_anno`: ddl per anno di presentazione
- `mart_iter_tempi`: tempi dell'iter per i ddl diventati legge (media 295 giorni, max 3,7 anni)

## Criterio di promozione

Promuovere quando: (1) la distribuzione per stato è verificata; (2) il join con i ddl presentati alla Camera (via `rif_deputato`) è esplorato; (3) una domanda civica usa i dati (es. ddl fermi in commissione).

## Stato / prossimo passo

- **Stato**: candidate a standard v1 (2026-08-03) — issue #781, XIX legislatura
- **Prossimo passo**: run + verifica, poi PR; estensione a legislature 13-19
