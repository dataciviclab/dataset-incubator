SELECT 
    codice_territorio,
    codice_reato,
    anno,
    numero_denunce
FROM clean_input
ORDER BY anno, codice_territorio;