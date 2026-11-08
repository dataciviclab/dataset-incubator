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
        -- Il prospetto numera i livelli in cifre romane ("A.I)", "A.I.1.a)",
        -- "B.II.7.e.1)"), non in cifre arabe come il Conto Economico.
        regexp_extract(
            descrizione_voce, '^([A-Z](?:\.[IVXLCDM]+|\.[0-9]+|\.[a-z])*)\)', 1
        ) as _prefisso
    from base
),

livelli as (
    select
        *,
        -- profondità: "A" -> 0 (sezione), "A.I" -> 1, "A.I.1.a" -> 3
        case
            when _prefisso = '' then null
            else length(_prefisso) - length(replace(_prefisso, '.', ''))
        end as livello,
        -- voce di primo livello: "A.I", "B.II"; per le sezioni è la lettera
        case
            when _prefisso = '' then null
            when strpos(_prefisso, '.') = 0 then _prefisso
            else regexp_extract(_prefisso, '^([A-Z]\.[IVXLCDM]+|[A-Z]\.[0-9]+)', 1)
        end as voce_livello1
    from derived
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
    livello,
    voce_livello1,
    importo,
    data_aggiornamento
from livelli
where anno is not null
