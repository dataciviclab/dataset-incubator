-- mart_cittadinanze: acquisizioni di cittadinanza italiana per anno x
-- territorio x ex-cittadinanza x processo.
--
-- `aggregato` = true per le righe che NON sono "leaf" (territorio macro o
-- cittadinanza non-paese). Per numeri non gonfiati:
--   - TOTALE nazionale: `livello='nazionale' AND cittadinanza_codice='WORLD' AND processo_codice='ALL'`
--   - dettaglio sommabile: `WHERE NOT aggregato` (regione x paese reale)
-- `processo` include la riga aggregata 'Totale' oltre a Matrimonio/Residenza/Altro.

select
    anno,
    livello,
    territorio_codice,
    territorio,
    cittadinanza_codice,
    cittadinanza,
    processo_codice,
    processo,
    aggregato,
    acquisizioni
from clean_input
where acquisizioni is not null
order by anno, livello, territorio_codice, cittadinanza_codice, processo_codice
