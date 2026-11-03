-- mart_migrazioni: immigrazioni (trasferimenti di residenza dall'estero) per
-- anno x territorio di destinazione.
--
-- `aggregato` = true per i territori macro (nazionale/ripartizione, Trentino-
-- Alto Adige, ITTOT). Per numeri non gonfiati:
--   - TOTALE nazionale: `livello='nazionale' AND territorio_codice='IT'`
--   - dettaglio sommabile: `WHERE NOT aggregato` (province)

select
    anno,
    livello,
    territorio_codice,
    territorio,
    aggregato,
    immigrazioni
from clean_input
where immigrazioni is not null
order by anno, livello, territorio_codice
