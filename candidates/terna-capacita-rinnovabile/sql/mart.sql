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

SELECT 
    '2022' as anno,
    regione,
    provincia,
    capacita_installata_mw
FROM {{ ref('terna_raw', year=2022) }}

UNION ALL

SELECT 
    '2023' as anno,
    regione,
    provincia,
    capacita_installata_mw
FROM {{ ref('terna_raw', year=2023) }}

UNION ALL

SELECT 
    '2024' as anno,
    regione,
    provincia,
    capacita_installata_mw
FROM {{ ref('terna_raw', year=2024) }}