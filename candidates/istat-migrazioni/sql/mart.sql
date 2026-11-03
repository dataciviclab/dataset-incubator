-- mart_migrazioni: immigrazioni (trasferimenti di residenza) per anno x
-- territorio di destinazione.
--
-- Il mart contiene TUTTI i livelli territoriali (nazionale, ripartizione,
-- regione, provincia), marcati in `livello`: per sommare senza doppio
-- conteggio filtrare `WHERE livello = 'provincia'` (o il livello desiderato).

select
    anno,
    livello,
    territorio_codice,
    territorio,
    immigrazioni
from clean_input
where immigrazioni is not null
order by anno, livello, territorio_codice
