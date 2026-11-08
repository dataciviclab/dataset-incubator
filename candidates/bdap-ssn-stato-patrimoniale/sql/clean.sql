-- Stato Patrimoniale degli enti del SSN, livello regionale (OpenBDAP).
-- Una riga = una voce del prospetto per regione e anno, come pubblicata.
-- Il codice è a 6 caratteri: 1 = prospetto (A attivo / P passivo),
-- 2 = sezione, 3 = 'Z' per i totali di sezione.
with base as (
    select
        cast_int("Anno di Riferimento") as anno,
        normalize_string("Codice Regione") as codice_regione,
        normalize_string("Descrizione Regione") as descrizione_regione,
        upper(normalize_string("Codice Voce Contabile")) as codice_voce,
        regexp_replace(normalize_string("Descrizione Voce Contabile"), '\s+', ' ', 'g')
            as descrizione_voce,
        cast_double("Importo Totale") as importo,
        normalize_string("Data Aggiornamento") as data_aggiornamento
    from raw_input
),

derived as (
    select
        *,
        case when substr(codice_voce, 1, 1) = 'A' then 'attivo' else 'passivo' end as prospetto,
        substr(codice_voce, 1, 2) as sezione,
        substr(codice_voce, 3, 1) = 'Z' as riga_sintesi,
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
    prospetto,
    sezione,
    riga_sintesi,
    -- profondità della voce: "A.I)" -> 1, "A.I.1.a)" -> 2, ...
    -- null per le righe di sintesi senza prefisso (es. "D) TOTALE ATTIVO").
    case
        when _prefisso = '' then null
        else length(_prefisso) - length(replace(_prefisso, '.', ''))
    end as livello,
    nullif(voce_livello1, '') as voce_livello1,
    importo,
    data_aggiornamento
from derived
where anno is not null
