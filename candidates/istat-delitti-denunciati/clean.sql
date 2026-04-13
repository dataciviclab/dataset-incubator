-- 1. Preparazione ambiente
INSTALL xml;
LOAD xml;

-- Creiamo la tabella leggendo direttamente il file XML (che si chiama .csv)
CREATE OR REPLACE TABLE clean_delitti AS 
SELECT * FROM read_xml(
    'out/data/raw/istat-delitti-denunciati/2024/delitti_raw.csv',
    global_settings={'flatten_all_nodes': true}
);