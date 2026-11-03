-- mart_cittadinanze: acquisizioni di cittadinanza italiana per anno x
-- territorio x ex-cittadinanza x processo di acquisizione.
--
-- Il mart contiene TUTTI i livelli territoriali (nazionale, ripartizione,
-- regione, provincia), marcati in `livello`: per sommare senza doppio
-- conteggio filtrare `WHERE livello = 'provincia'` (o il livello desiderato).
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
    acquisizioni
from clean_input
where acquisizioni is not null
order by anno, livello, territorio_codice, cittadinanza_codice, processo_codice
