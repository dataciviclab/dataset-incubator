SELECT 
    CAST("Anno" AS INTEGER) as anno,
    "Tipo capacità" as tipo_capacita,
    "Regione" as regione,
    "Provincia" as provincia,
    "Fonti" as fonti,
    CAST("Potenza efficiente (MW)" AS FLOAT) as potenza_mw
FROM raw_input
WHERE "Anno" IS NOT NULL 
  AND CAST("Anno" AS STRING) NOT LIKE 'Applied%'