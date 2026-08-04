# senato-anagrafica

**Domanda guida:** Chi sono i senatori della XIX legislatura? Quando e dove sono nati? A quale `senatore_id` corrisponde ogni nome?

**Fonte:** Senato della Repubblica — OpenData SPARQL (`https://dati.senato.it/sparql`)
**Dataset:** graph `composizione/19` (XIX legislatura), classe `osr:Senatore` (341 senatori)
**Licenza:** CC BY 3.0

## Perché vale la pena

`senato_firmatari` espone `senatore_id` (oltre 3.000 valori) senza alcuna anagrafica joinabile. Questo support dataset chiude il ramo Senato delle persone: nome, cognome, data e luogo di nascita. Join con `senato_firmatari` via `senatore_id`.

## Output minimo atteso

- `senato_anagrafica`: senatore_id, nome, cognome, data_nascita, luogo_nascita, legislatura — ~341 righe
- `mart_nascita_anno`: distribuzione età
- `mart_luogo_nascita`: top città di nascita

## Criterio di promozione

Promuovere quando il join con `senato_firmatari` (via `senatore_id`) è verificato e una domanda civica usa l'anagrafica senatori.

## Stato / prossimo passo

- **Stato**: support a standard v1 (2026-08-04)
- **Prossimo passo**: run + verifica join con senato_firmatari; estensione a legislature 13-19
