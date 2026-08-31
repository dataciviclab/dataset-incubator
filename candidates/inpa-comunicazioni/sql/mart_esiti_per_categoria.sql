-- Mart esiti: comunicazioni per categoria (ciclo di vita dei concorsi)
SELECT
    categoria,
    COUNT(*) AS num_comunicazioni
FROM clean_input
WHERE categoria IS NOT NULL
GROUP BY categoria
ORDER BY num_comunicazioni DESC
