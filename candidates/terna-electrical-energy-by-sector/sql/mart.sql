-- mart.sql - terna_electrical_energy_by_sector - mart_consumi_settore_provincia
-- Consumi elettrici per anno, provincia e settore
-- Nota: gli anni 2015-2020 hanno dati disaggregati (piu righe per provincia/settore),
-- il SUM le aggrega correttamente. Il dato e' comparabile con 2021-2024 (gia aggregato).

SELECT
    anno,
    regione,
    provincia,
    settore,
    ROUND(SUM(consumo_gwh), 3) AS consumo_totale_gwh
FROM clean_input
GROUP BY anno, regione, provincia, settore
ORDER BY anno DESC, regione, provincia, settore
