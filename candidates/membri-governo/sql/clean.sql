-- clean.sql — membri_governo
--
-- Membri e organi dei Governi italiani dal Regno d'Italia (1862) alla XIX
-- legislatura. Input: CSV da endpoint SPARQL dati.camera.it (una riga = un
-- membro del governo, già deduplicato con GROUP BY + MAX lato query).
--
-- persona_id: chiave standard del sistema parlamentare (id numerico
-- dall'URI persona.rdf/p5660 → 5660, pr20 → 20) — ponte verso deputati,
-- senato, incarichi. Stessa normalizzazione di camera_deputati_legislature.
--
-- Nota: i membri del Regno (URI mgr...) hanno ruolo e start_date NON
-- valorizzati — la data è solo nella label ("dal 21.06.1894 al 01.12.1894").
-- Decisione: ruolo/start_date NULL per il Regno (parsing label opzionale futuro).

WITH base AS (
    SELECT
        membro,
        ruolo,
        label,
        start,
        "end",
        interim,
        motivoTermine,
        persona,
        nome,
        cognome,
        legislatura,
        governo,
        organo
    FROM raw_input
)
SELECT
    normalize_string(membro)                                          AS membro,
    -- id numerico della persona dall'URI (p5660 Repubblica, pr20 Regno)
    TRY_CAST(
        CASE
            WHEN persona LIKE '%/persona.rdf/p%' AND persona NOT LIKE '%/persona.rdf/pr%' THEN
                regexp_extract(persona, 'persona\.rdf/p(\d+)', 1)
            WHEN persona LIKE '%/persona.rdf/pr%' THEN
                regexp_extract(persona, 'persona\.rdf/pr(\d+)', 1)
        END AS BIGINT
    )                                                                 AS persona_id,
    normalize_string(ruolo)                                           AS ruolo,
    normalize_string(label)                                           AS label,
    -- start: YYYYMMDD (BIGINT da sniff DuckDB, stringhe vuote → NULL) → DATE
    TRY_CAST(
        CASE WHEN start IS NOT NULL
             THEN substr(CAST(start AS VARCHAR), 1, 4) || '-' ||
                  substr(CAST(start AS VARCHAR), 5, 2) || '-' ||
                  substr(CAST(start AS VARCHAR), 7, 2)
        END AS DATE
    )                                                                 AS start_date,
    -- end: stessa codifica YYYYMMDD → DATE (membri cessati; NULL = in carica)
    TRY_CAST(
        CASE WHEN "end" IS NOT NULL
             THEN substr(CAST("end" AS VARCHAR), 1, 4) || '-' ||
                  substr(CAST("end" AS VARCHAR), 5, 2) || '-' ||
                  substr(CAST("end" AS VARCHAR), 7, 2)
        END AS DATE
    )                                                                 AS end_date,
    -- interim: flag "ad interim" (0/1 dalla fonte)
    TRY_CAST(interim AS BOOLEAN)                                      AS interim,
    normalize_string(motivoTermine)                                   AS motivo_termine,
    normalize_string(nome)                                            AS nome,
    normalize_string(cognome)                                         AS cognome,
    -- legislatura: URI ocd/legislatura.rdf/repubblica_17 → "repubblica_17"
    CASE
        WHEN legislatura LIKE '%/legislatura.rdf/%' THEN
            substring(legislatura, strpos(legislatura, '/legislatura.rdf/') + 17)
        ELSE legislatura
    END                                                               AS legislatura,
    normalize_string(governo)                                         AS governo,
    normalize_string(organo)                                          AS organo
FROM base
WHERE membro IS NOT NULL
