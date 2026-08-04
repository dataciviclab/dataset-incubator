# senato-firmatari — Firmatari dei disegni di legge del Senato

## Domanda civica

"Da quali senatori nascono i disegni di legge?" (issue #781) — i ddl del Senato
non hanno solo uno stato: hanno dei presentatori. Chi firma i ddl? Quanti ne
firmano per legislatura? Iniziativa parlamentare o governativa?

## Dataset / fonte

- Fonte: endpoint SPARQL Senato (`dati.senato.it`), graph `ddl/19` (XIX legislatura)
- Support dataset di `senato-ddl`: arricchisce il ddl con i suoi presentatori
- Una riga = una coppia (ddl, iniziativa) — un ddl può avere più presentatori

## Perché vale la pena

Il dataset `senato-ddl` risponde "in che stato è il ddl" ma non "chi lo ha
presentato". Questo support chiude la domanda #781: il join avviene su `ddl_id`.

## Output minimo atteso

- `mart_firmatari_ddl`: ddl con numero di presentatori (e primi firmatari)
- `mart_tipo_iniziativa`: distribuzione Parlamentare / Governativa

## Criterio di promozione

Promuovere quando il join con `senato-ddl` (via `ddl_id`) è verificato e una
domanda civica usa i firmatari.

## Stato / prossimo passo

- **Stato**: candidate a standard v1 (2026-08-04) — issue #781
- **Prossimo passo**: run + verifica, poi PR con `senato-ddl`
