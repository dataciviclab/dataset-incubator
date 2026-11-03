-- mart_permessi: permessi di soggiorno validi (stock al 1 gennaio) per anno x
-- territorio x cittadinanza.
--
-- Il mart contiene TUTTI i livelli territoriali (nazionale, ripartizione,
-- regione, provincia), marcati in `livello`: per sommare senza doppio
-- conteggio filtrare `WHERE livello = 'provincia'` (o il livello desiderato).
-- ATTENZIONE: la dimensione cittadinanza include anche AGGREGATI (aree
-- geopolitiche: Africa, Asia, ... e il totale). Per i singoli paesi filtrare
-- i codici ISO-3166 alpha-2 (2 lettere).

select
    anno,
    livello,
    territorio_codice,
    territorio,
    cittadinanza_codice,
    cittadinanza,
    permessi
from clean_input
where permessi is not null
order by anno, livello, territorio_codice, cittadinanza_codice
