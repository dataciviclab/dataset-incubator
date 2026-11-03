-- mart_stranieri_residenti: stranieri residenti al 1 gennaio per anno x
-- territorio x cittadinanza.
--
-- `aggregato` = true per le righe che NON sono "leaf" (territorio macro o
-- cittadinanza non-paese). Per numeri non gonfiati:
--   - TOTALE nazionale: `livello='nazionale' AND cittadinanza_codice='WORLD'`
--   - dettaglio sommabile: `WHERE NOT aggregato` (provincia x paese reale)

select
    anno,
    livello,
    territorio_codice,
    territorio,
    cittadinanza_codice,
    cittadinanza,
    aggregato,
    residenti
from clean_input
where residenti is not null
order by anno, livello, territorio_codice, cittadinanza_codice
