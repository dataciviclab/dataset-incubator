-- Conto Economico degli enti del SSN, livello regionale (OpenBDAP).
-- Un riga = un conto del CE per regione e anno, così come pubblicato dalla fonte.
-- Il file raw è ";", cp1252, con una colonna vuota di troppo in coda (gestita
-- da strict_mode: false). Le voci sono una gerarchia indentata nella descrizione
-- ("A.1)", "A.1.A)", "A.1.A.1)"), non nel codice: qui si esplicita il livello.
with base as (
    select
        try_cast("Anno di Riferimento" as integer) as anno,
        trim("Codice Regione") as codice_regione,
        trim("Descrizione Regione") as descrizione_regione,
        upper(trim("Codice Voce Contabile")) as codice_voce,
        regexp_replace(trim("Descrizione Voce Contabile"), '\s+', ' ', 'g') as descrizione_voce,
        try_cast("Importo Totale" as double) as importo,
        try_cast(strptime(trim("Data Aggiornamento"), '%d/%m/%Y') as date) as data_aggiornamento
    from raw_input
),

derived as (
    select
        *,
        substr(codice_voce, 1, 1) as sezione,
        substr(codice_voce, 2, 1) = 'Z' as riga_sintesi,
        -- prefisso gerarchico della voce: "A.1", "A.9.B", "A.1.A.1.1".
        -- Deve ammettere segmenti alfabetici (A.9.B) e numerici (B.10).
        regexp_extract(descrizione_voce, '^([A-Z]\.\d+(?:\.[A-Z0-9]+)*)', 1) as _prefisso,
        regexp_extract(descrizione_voce, '^([A-Z]\.\d+)', 1) as voce_livello1
    from base
)

select
    anno,
    codice_regione,
    descrizione_regione,
    codice_voce,
    descrizione_voce,
    sezione,
    riga_sintesi,
    -- profondità della voce nella gerarchia CE: A.1 -> 1, A.9.B -> 2, ...
    -- null per le righe di sintesi senza prefisso (es. XA0000, ZZ9999).
    case
        when _prefisso = '' then null
        else length(_prefisso) - length(replace(_prefisso, '.', ''))
    end as livello,
    nullif(voce_livello1, '') as voce_livello1,
    importo,
    data_aggiornamento
from derived
