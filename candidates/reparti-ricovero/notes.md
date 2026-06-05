# Note — reparti-ricovero

## Rischi noti
- `num_dimessi` e `giornate_degenza` con punto separatore migliaia → restano VARCHAR (`_raw`)
- decimal="," per valori con virgola (es. tassi)
- Fonte B non entra nel compose principale di malasanita (ridondante con C sui posti letto aggregati)
- Valore aggiunto: dettaglio per disciplina/reparto (mart_regioni_disciplina)
