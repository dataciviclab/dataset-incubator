-- Macro toolkit: normalize_string
SELECT
    normalize_string(cig) AS cig,
    normalize_string(cup) AS cup
FROM raw_input
WHERE cig IS NOT NULL AND cup IS NOT NULL
  AND TRIM(cig) != '' AND TRIM(cup) != ''
