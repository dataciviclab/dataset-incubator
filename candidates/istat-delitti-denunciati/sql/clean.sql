-- candidates/istat-delitti-denunciati/sql/clean.sql
SELECT 
    regexp_extract(CAST(content AS VARCHAR), '(<.*)', 1) as payload_xml
FROM read_blob('out/data/raw/istat-delitti-denunciati/2024/temp/delitti_raw.txt');