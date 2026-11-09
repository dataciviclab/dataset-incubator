-- Conto Economico degli enti del SSN, livello per ente (OpenBDAP).
-- Una riga = una voce del CE per ente e anno, come pubblicata.
-- Il codice è a 6 caratteri: 1 = sezione (A ricavi, B costi, ...),
-- 2 = 'Z' per i totali di sezione.
with base as (
    select
        cast_int("Anno di Riferimento") as anno,
        normalize_string("Codice Regione") as codice_regione,
        normalize_string("Descrizione Regione") as descrizione_regione,
        normalize_string("Tipo Rilevazione") as tipo_rilevazione,
        normalize_string("Codice Ente SSN") as codice_ente_ssn,
        normalize_string("Codice Ente BDAP") as codice_ente_bdap,
        normalize_string("Descrizione Ente") as descrizione_ente,
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
        substr(codice_voce, 1, 1) as sezione,
        substr(codice_voce, 2, 1) = 'Z' as riga_sintesi,
        -- 000 = ente regione, 999 = consolidato regionale. Convenzione
        -- invertita rispetto al modello LEA: qui 000 è un soggetto reale.
        case
            when codice_ente_ssn = '000' then 'regione'
            when codice_ente_ssn = '999' then 'consolidato'
            else 'ente'
        end as tipo_riga,
        -- Il CE numera i livelli in cifre arabe: "A.1)", "A.1.A)", "B.10)".
        regexp_extract(
            descrizione_voce, '^([A-Z]\.\d+(?:\.[A-Z0-9]+)*)', 1
        ) as _prefisso
    from base
),

livelli as (
    select
        *,
        case
            when _prefisso = '' then null
            else length(_prefisso) - length(replace(_prefisso, '.', ''))
        end as livello,
        nullif(regexp_extract(_prefisso, '^([A-Z]\.\d+)', 1), '') as voce_livello1
    from derived
)

select
    anno,
    codice_regione,
    descrizione_regione,
    tipo_rilevazione,
    codice_ente_ssn,
    codice_ente_bdap,
    descrizione_ente,
    tipo_riga,
    codice_voce,
    descrizione_voce,
    sezione,
    riga_sintesi,
    livello,
    voce_livello1,
    importo,
    data_aggiornamento
from livelli
where anno is not null
