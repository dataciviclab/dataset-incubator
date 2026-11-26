-- Call UE aperte/in arrivo da SEDIA (Funding & Tenders Portal).
-- I topic possono avere deadline passata nonostante status Open: si marca
-- ha_scadenza_futura per filtrare nel mart. Dedup su identifier già in extract.
-- Date: normalize_string (TRIM + ''→NULL) poi TRY_CAST DATE — disattiva
-- l'inferimento DATE del CSV reader sui campi vuoti.
WITH base AS (
    SELECT
        normalize_string(identifier) AS identifier,
        normalize_string(call_identifier) AS call_identifier,
        normalize_string(call_title) AS call_title,
        normalize_string(title) AS title,
        normalize_string(status) AS status,
        normalize_string(status_label) AS status_label,
        normalize_string(framework_programme) AS framework_programme,
        normalize_string(framework_label) AS framework_label,
        normalize_string(programme_period) AS programme_period,
        normalize_string(types_of_action) AS types_of_action,
        TRY_CAST(normalize_string(start_date) AS DATE) AS start_date,
        TRY_CAST(normalize_string(deadline_date) AS DATE) AS deadline_date,
        normalize_string(deadline_model) AS deadline_model,
        cast_double(normalize_string(budget_total_eur)) AS budget_total_eur,
        cast_bigint(normalize_string(expected_grants)) AS expected_grants,
        normalize_string(url) AS url
    FROM raw_input
    WHERE normalize_string(identifier) IS NOT NULL
)
SELECT
    *,
    CASE
        WHEN deadline_date IS NULL THEN NULL
        ELSE CAST(deadline_date - CURRENT_DATE AS BIGINT)
    END AS giorni_alla_scadenza,
    CASE
        WHEN deadline_date IS NULL THEN false
        ELSE deadline_date >= CURRENT_DATE
    END AS ha_scadenza_futura
FROM base
