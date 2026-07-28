-- Mart: demografia candidati uninominali (Camera/Senato)
-- Ogni riga: circoscrizione × camera × anno
-- Copertura: Mattarellum (1994-2001, Camera) e Rosatellum (2018-2022, Camera+Senato)
--
-- Filtro composito per identificare righe uninominali:
--   - Rosatellum: collegio_uninominale valorizzato
--   - Mattarellum: cognome popolato su anno <= 2001
--     (in quelle tornate le righe proporzionali non hanno cognome)

WITH candidati_unici AS (
    SELECT DISTINCT
        data_elezione,
        EXTRACT(YEAR FROM data_elezione) AS anno,
        camera_senato,
        circoscrizione,
        cognome,
        nome,
        sesso,
        luogo_nascita,
        data_nascita
    FROM clean_input
    WHERE cognome IS NOT NULL AND cognome != ''
      AND (
          (collegio_uninominale IS NOT NULL AND collegio_uninominale != '')
          OR (EXTRACT(YEAR FROM data_elezione) BETWEEN 1994 AND 2001)
      )
),

candidati_con_eta AS (
    SELECT *,
        CASE
            WHEN REGEXP_MATCHES(data_nascita, '^\d{4}-\d{2}-\d{2}')
            THEN EXTRACT(YEAR FROM CAST(data_nascita AS DATE))
            WHEN REGEXP_MATCHES(data_nascita, '^\d{2}/\d{2}/\d{4}')
            THEN CAST(SUBSTRING(data_nascita, 7, 4) AS BIGINT)
        END AS anno_nascita
    FROM candidati_unici
),

candidati_eta AS (
    SELECT *,
        CASE WHEN anno_nascita IS NOT NULL AND anno_nascita > 1800
            THEN anno - anno_nascita
        END AS eta_elezione
    FROM candidati_con_eta
),

stats AS (
    SELECT
        data_elezione, anno, camera_senato, circoscrizione,
        COUNT(*) AS n_candidati,
        COUNT(DISTINCT CASE WHEN sesso = 'M' THEN cognome || nome END) AS candidati_m,
        COUNT(DISTINCT CASE WHEN sesso = 'F' THEN cognome || nome END) AS candidati_f,
        ROUND(AVG(eta_elezione), 1) AS eta_media,
        ROUND(MIN(eta_elezione), 0) AS eta_min,
        ROUND(MAX(eta_elezione), 0) AS eta_max,
        CASE WHEN COUNT(DISTINCT cognome || nome) > 0 THEN
            ROUND(COUNT(DISTINCT CASE WHEN eta_elezione < 40 THEN cognome || nome END) * 100.0 / COUNT(DISTINCT cognome || nome), 1)
        END AS under40_pct,
        CASE WHEN COUNT(DISTINCT cognome || nome) > 0 THEN
            ROUND(COUNT(DISTINCT CASE WHEN eta_elezione >= 60 THEN cognome || nome END) * 100.0 / COUNT(DISTINCT cognome || nome), 1)
        END AS over60_pct
    FROM candidati_eta
    GROUP BY data_elezione, anno, camera_senato, circoscrizione
)

SELECT s.*,
    ROUND(s.candidati_f * 100.0 / NULLIF(s.n_candidati, 0), 1) AS quota_femminile_pct
FROM stats s
ORDER BY s.anno DESC, s.camera_senato, s.circoscrizione
