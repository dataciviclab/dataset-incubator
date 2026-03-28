SELECT 
    anno,
    regione,
    provincia,
    fonti,
    SUM(potenza_mw) as potenza_totale_mw
FROM clean
WHERE tipo_capacita = 'Lorda'
GROUP BY 1, 2, 3, 4
