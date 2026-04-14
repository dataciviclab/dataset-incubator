WITH raw_blob AS (
    SELECT content as xml_content
    FROM read_text('out/data/raw/istat-delitti-denunciati/2024/delitti_raw.txt')
),
series AS (
    -- Estraiamo ogni blocco <generic:Series>
    SELECT unnest(regexp_extract_all(xml_content, '(?s)<generic:Series>.*?</generic:Series>')) as s
    FROM raw_blob
),
observations AS (
    -- Per ogni Series, estraiamo le singole osservazioni <generic:Obs>
    SELECT 
        s,
        unnest(regexp_extract_all(s, '(?s)<generic:Obs>.*?</generic:Obs>')) as o
    FROM series
)
SELECT 
    -- Estraiamo i codici dai tag <generic:Value id="..." value="..." />
    regexp_extract(s, '<generic:Value id="REF_AREA" value="([^"]*)"', 1) as codice_territorio,
    regexp_extract(s, '<generic:Value id="TYPE_CRIME" value="([^"]*)"', 1) as codice_reato,
    -- Estraiamo l'anno e il valore dai tag Obs
    regexp_extract(o, '<generic:ObsDimension id="TIME_PERIOD" value="([^"]*)"', 1) as anno,
    TRY_CAST(regexp_extract(o, '<generic:ObsValue value="([^"]*)"', 1) AS DOUBLE) as numero_denunce
FROM observations
-- Filtriamo solo l'anno 2024 (o quello che ti serve) e puliamo i null
WHERE anno = '2024' 
  AND codice_territorio IS NOT NULL;