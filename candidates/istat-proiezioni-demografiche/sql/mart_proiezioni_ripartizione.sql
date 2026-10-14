-- Mart: popolazione proiettata aggregata per ripartizione geografica
-- Complemento al mart dettagliato: quadro sintetico Nord/Centro/Sud
SELECT
    anno,
    CASE
        WHEN territorio_codice IN ('ITC', 'ITC1', 'ITC2', 'ITC3', 'ITC4',
                                   'ITH', 'ITH1', 'ITH2', 'ITH3', 'ITH4', 'ITH5')
            THEN 'Nord'
        WHEN territorio_codice IN ('ITI', 'ITI1', 'ITI2', 'ITI3', 'ITI4')
            THEN 'Centro'
        WHEN territorio_codice IN ('ITF', 'ITF1', 'ITF2', 'ITF3', 'ITF4', 'ITF5', 'ITF6',
                                   'ITG', 'ITG1', 'ITG2')
            THEN 'Sud e Isole'
        ELSE 'altro'
    END AS ripartizione,
    sum(popolazione) AS popolazione
FROM clean_input
WHERE territorio_codice NOT LIKE 'IT%'
   OR territorio_codice IN ('ITC', 'ITH', 'ITI', 'ITF', 'ITG')
   OR (length(territorio_codice) = 5 AND territorio_codice LIKE 'IT%')
GROUP BY anno, 2
HAVING ripartizione != 'altro'
ORDER BY anno, ripartizione
