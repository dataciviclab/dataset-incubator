-- CUP: distribuzione CIG per CUP
-- Quanti CIG mediamente per CUP? Quali CUP hanno più gare?
SELECT
    cup,
    COUNT(*) AS n_cig,
    COUNT(DISTINCT cig) AS n_cig_distinti
FROM clean_input
GROUP BY cup
ORDER BY n_cig DESC
