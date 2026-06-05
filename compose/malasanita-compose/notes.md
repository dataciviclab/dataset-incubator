# Note — malasanita-compose

## Stato tecnico

Compose puro standalone (non più annidato in candidate A come nella vecchia architettura).
Join A+C+D verificato: 21/21 regioni per tutte e 3 le versioni (v1/v2/v3).

## Fonte D — metodologia

La fonte D è il punto metodologicamente più delicato:

- **v1**: mortalità totale 30+ (`cod_causa=25`) — baseline storica
- **v2**: 12 cause Euro-2013 (amenable + preventable), tasso grezzo 30+ — proxy di supporto
- **v3**: stesse 12 cause, ma con age-standardizzazione broad su 3 bande (30-69, 70-84, 85+) con pesi ESP2013 aggregati — **baseline raccomandata**

Il ranking regionale cambia tra v2 e v3 per via dell'artefatto demografico (es. Liguria #1 in v2 → #9 in v3).

## Join regionale

- Fonte A e C: `codice_regione` a 3 cifre Ministero (es. `"010"`)
- Fonte D: `cod_territorio` ISTAT a 2 cifre (es. `"01"`)
- Mapping: `LEFT(codice_regione, 2)` per regioni ordinarie, `041→21` (Bolzano), `042→22` (Trento)

## Rischi noti

- **Fonte D**: i 3 mart (v1/v2/v3) sono letti con `union_by_name=true`. La v3 viene filtrata per presenza di `tasso_std_broad_evitabile_10000_30plus`. Se in futuro D cambiasse schema, il filtro potrebbe non funzionare.
- **Separatore migliaia**: i CSV di C usano `.` come separatore migliaia — gestito dal toolkit v1.24.0+ con `decimal: ","` + `thousands: "."`
- **URL fonte A e C**: puntano a `dati.salute.gov.it`, bloccato in CI senza proxy
