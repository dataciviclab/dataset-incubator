-- mart_merci_per_direttrice.sql: tonnellate-km per coppia origine->destinazione.
-- OSSERVAZIONE (2026-11-03): le coppie regione->regione NON esistono nei dati.
-- Quello che c'e' e' regione->Italia e Italia->regione: la dimensione O-D e'
-- parziale, non una matrice completa. Filtrare su due codici NUTS2 restituisce
-- zero righe. Il mart tiene quindi entrambi i versi, con un lato a 'IT'.

select
    anno,
    regione_carico,
    regione_scarico,
    sum(valore) as tonnellate_km
from clean_input
where unita = 'GC_TKM'
  and regione_carico  like 'IT%'
  and regione_scarico like 'IT%'
  and regione_carico <> regione_scarico
group by 1, 2, 3
order by tonnellate_km desc
