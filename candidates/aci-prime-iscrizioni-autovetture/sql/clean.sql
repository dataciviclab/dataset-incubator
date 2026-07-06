SELECT anno, comune, provincia, alimentazione, prime_iscrizioni
FROM (
  SELECT 2017 AS anno, enteTerritoriale AS comune, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER) AS prime_iscrizioni
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2017.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2018, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2018.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2019, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2019.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2020, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2020.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2021, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2021.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2022, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2022.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2023, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2023.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
  UNION ALL
  SELECT 2024, enteTerritoriale, provincia, alimentazione, TRY_CAST(primeIscrizioni AS INTEGER)
  FROM READ_CSV_AUTO('{root}/data/raw/aci_prime_iscrizioni_autovetture/2024/aci_2024.csv')
  WHERE tipoEnteTerritoriale = 'Comune'
)
