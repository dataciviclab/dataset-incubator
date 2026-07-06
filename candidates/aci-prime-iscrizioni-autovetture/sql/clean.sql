SELECT 2017 AS anno, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER) AS prime_iscrizioni
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2017.csv')
UNION ALL
SELECT 2018, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2018.csv')
UNION ALL
SELECT 2019, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2019.csv')
UNION ALL
SELECT 2020, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2020.csv')
UNION ALL
SELECT 2021, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2021.csv')
UNION ALL
SELECT 2022, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2022.csv')
UNION ALL
SELECT 2023, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2023.csv')
UNION ALL
SELECT 2024, tipoEnteTerritoriale, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2024.csv')
