-- mart_permessi: permessi di soggiorno validi (stock al 1 gennaio) per anno x
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
    permessi
from clean_input
where permessi is not null
order by anno, livello, territorio_codice, cittadinanza_codice
