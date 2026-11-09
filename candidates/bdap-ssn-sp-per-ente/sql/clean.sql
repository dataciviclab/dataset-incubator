-- Stato Patrimoniale degli enti del SSN, livello per ente (OpenBDAP).
-- Una riga = una voce del prospetto per ente e anno, come pubblicata.
--Il codice è a 6 caratteri: 1 = prospetto (A attivo / P passivo),
-- 2 = sezione, 3 = 'Z' per i totali di sezione.
with base as (
    select
        cast_int("Anno di Riferimento") as anno,
        normalize_string("Codice Regione") as codice_regione,
        normalize_string("Descrizione Regione") as descrizione_regione,
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
        case when substr(codice_voce, 1, 1) = 'A' then 'attivo' else 'passivo' end as prospetto,
        substr(codice_voce, 1, 2) as sezione,
        substr(codice_voce, 3, 1) = 'Z' as riga_sintesi,
        -- 000 = ente regione, 999 = consolidato regionale. La convenzione è
        -- invertita rispetto al modello LEA: qui 000 è un soggetto reale.
        case
            when codice_ente_ssn = '000' then 'regione'
            when codice_ente_ssn = '999' then 'consolidato'
            else 'ente'
        end as tipo_riga,
        -- Il prospetto numera i livelli in cifre romane ("A.I)", "A.I.1.a)").
        regexp_extract(
            descrizione_voce, '^([A-Z](?:\.[IVXLCDM]+|\.[0-9]+|\.[a-z])*)\)', 1
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
    codice_ente_ssn,
    codice_ente_bdap,
    descrizione_ente,
    tipo_riga,
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
