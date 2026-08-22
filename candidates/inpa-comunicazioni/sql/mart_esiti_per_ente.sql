-- Mart esiti: comunicazioni per ente (chi pubblica esiti)
SELECT
    ente,
    COUNT(*) AS num_comunicazioni
FROM clean_input
WHERE ente IS NOT NULL
GROUP BY ente
ORDER BY num_comunicazioni DESC
