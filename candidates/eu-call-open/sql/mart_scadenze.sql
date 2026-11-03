-- Call con scadenza futura, ordinate per imminenza.
-- Include anche open con deadline passata come righe "scadute" se filtrate a valle;
-- di default il mart espone solo ha_scadenza_futura = true (gap "in scadenza").
SELECT
    identifier,
    deadline_date,
    giorni_alla_scadenza,
    call_identifier,
    title,
    framework_programme,
    framework_label,
    types_of_action,
    status_label,
    budget_total_eur,
    expected_grants,
    url
FROM clean_input
WHERE ha_scadenza_futura = true
ORDER BY deadline_date, budget_total_eur DESC NULLS LAST, call_identifier
