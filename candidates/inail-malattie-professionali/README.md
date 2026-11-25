# inail-malattie-professionali

## Domanda civica

**Quali malattie professionali colpiscono i lavoratori italiani, in quali settori e con quale gravità?**

L'INAIL registra le malattie professionali denunciate: agente causale, settore economico, ICD10, grado di menomazione, indennizzi. Nessun dataset nel Lab copre questa dimensione della sicurezza sul lavoro.

## Dataset / fonte

- **Fonte**: `inail_opendata` — dati.inail.it (CKAN + CSV diretti)
- **Dataset**: Malattie professionali semestrali per data protocollo, file Italia
- **Copertura**: snapshot al 2026-04-30, 375K casi
- **Unità di analisi**: singola denuncia di malattia professionale

## Perché vale la pena

- **Unica fonte su agente causale**: quali sostanze/attività causano malattie professionali in Italia
- **Settore × malattia**: join tra economia e sicurezza — nessun altro dataset del Lab lo offre
- **Grado menomazione + indennizzi**: gravità umana del fenomeno, non solo conteggi
- **ICD10 denunciato vs accertato**: differenza tra percezione e accertamento medico

## Output minimo atteso

| Mart | Cosa risponde |
|------|---------------|
| `mart_casi_settore` | Quali settori hanno più malattie professionali? |
| `mart_casi_agente` | Quali agenti causali colpiscono quali settori? |
| `mart_menomazione` | Quanto sono gravi le menomazioni? |
| `mart_genere` | Uomini e donne sono colpiti diversamente? |

## Criterio di promozione

Promuovere a repo dati autonomo quando:
1. La serie viene aggiornata con il prossimo snapshot semestrale
2. Il join con minlavoro-flussi produce almeno un finding verificato
3. Gli infortuni (attualmente bloccati) tornano disponibili e si integra il quadro completo

## Stato / prossimo passo

- [x] Config + SQL
- [ ] Run e validazione
- [ ] Aggiornamento automatico snapshot (quando INAIL pubblica il prossimo)
- [ ] Integrazione con infortuni (quando tornano disponibili)
