-- candidates/istat-delitti-denunciati/sql/mart.sql

WITH base AS (
    SELECT 
        replace(linea, '\x5C\x22', '"') as xml_clean
    FROM clean_input
),
series AS (
    SELECT 
        unnest(regexp_extract_all(xml_clean, '(?s)<generic:Series.*?>.*?</generic:Series>')) as s
    FROM base
),
observations AS (
    SELECT 
        s as serie_full,
        unnest(regexp_extract_all(s, '(?s)<generic:Obs.*?>.*?</generic:Obs>')) as o
    FROM series
)
SELECT 
    -- Estrazione Codici (dalla Serie)
    regexp_extract(serie_full, 'id="REF_AREA"\s+value="([^"]*)"', 1) as codice_territorio,
    regexp_extract(serie_full, 'id="TYPE_CRIME"\s+value="([^"]*)"', 1) as codice_reato,
    
    -- Anno: cerchiamo specificamente il valore dentro ObsDimension
    regexp_extract(o, '<generic:ObsDimension[^>]*value="([^"]*)"', 1) as anno,

    -- Numero Denunce: cerchiamo specificamente il valore dentro ObsValue
    TRY_CAST(regexp_extract(o, '<generic:ObsValue[^>]*value="([^"]*)"', 1) AS DOUBLE) as numero_denunce

FROM observations
WHERE codice_territorio IS NOT NULL 
  AND numero_denunce IS NOT NULL;