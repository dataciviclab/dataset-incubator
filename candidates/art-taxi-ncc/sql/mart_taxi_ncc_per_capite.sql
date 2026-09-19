-- Mart: licenze TAXI/NCC per comune con ratio ogni 10.000 residenti.
-- Risponde a: quali comuni hanno più taxi/NCC in rapporto alla popolazione?
SELECT
    comune,
    taxi,
    ncc,
    popolazione_residente,
    ROUND(taxi * 10000.0 / NULLIF(popolazione_residente, 0), 2) AS taxi_per_10k,
    ROUND(ncc * 10000.0 / NULLIF(popolazione_residente, 0), 2) AS ncc_per_10k
FROM clean_input
