-- Conteggio call e budget aggregato per programma UE (framework).
SELECT
    framework_programme,
    framework_label,
    COUNT(*) AS n_call,
    SUM(CASE WHEN budget_total_eur IS NOT NULL THEN 1 ELSE 0 END) AS n_con_budget,
    SUM(COALESCE(budget_total_eur, 0)) AS budget_totale_eur,
    SUM(CASE WHEN ha_scadenza_futura THEN 1 ELSE 0 END) AS n_scadenza_futura
FROM clean_input
GROUP BY framework_programme, framework_label
ORDER BY n_call DESC, budget_totale_eur DESC
