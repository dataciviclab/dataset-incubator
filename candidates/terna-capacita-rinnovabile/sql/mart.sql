-- Questo file unisce i dati annuali di Terna in un unico dataset storico
-- Obiettivo: Fornire una serie storica 2020-2024 della capacità installata (MW) per provincia

SELECT 
    '2020' as anno,
    regione,
    provincia,
    capacita_installata_mw
FROM {{ ref('terna_raw', year=2020) }}

UNION ALL

SELECT 
    '2021' as anno,
    regione,
    provincia,
    capacita_installata_mw
FROM {{ ref('terna_raw', year=2021) }}

UNION ALL

-- ... e così via per gli altri anni (2022, 2023, 2024)
-- Nota: La funzione {{ ref(...) }} è quella che il toolkit del Lab usa 
-- per collegare le sorgenti definite nel tuo dataset.yml