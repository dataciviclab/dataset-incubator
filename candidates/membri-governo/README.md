# membri-governo

**Domanda guida:** Chi ha governato l'Italia? Quanti governi si sono succeduti dal Regno d'Italia (1862) a oggi, chi ne faceva parte, con quale ruolo, per quanto tempo e in quale legislatura?

**Fonte:** Camera dei Deputati — OpenData SPARQL (`https://dati.camera.it/sparql`)
**Dataset:** `ocd:membroGoverno` (7.579 membri, 160 anni di governi)
**Licenza:** CC BY 3.0

## Perché vale la pena

Il Lab ha DAIT (amministratori locali) e Camera (deputati), ma zero dati sui governi nazionali. Questo chiude il cerchio "chi governa": 160 anni di governi dal Regno alla Repubblica, con nomi, ruoli e date. Join naturale con `camera_deputati_legislature` via `persona_id`.

## Output minimo atteso

- `mart_legislatura`: membri/governi per legislatura (serie storica)
- `mart_governi`: composizione per governo (membri, durata)

## Criterio di promozione

Promuovere quando: (1) la serie storica per legislatura è verificata; (2) il join con deputati per persona_id è stabile; (3) una domanda civica usa i dati (es. durata media dei governi).

## Stato / prossimo passo

- **Stato**: candidate a standard v1 (2026-08-03) — issue #786
- **Prossimo passo**: run + verifica, poi PR
