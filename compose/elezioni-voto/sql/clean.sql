-- Clean: elezioni_voto — UNION ALL normalizzato dei 3 dataset elettorali
-- Legge i clean parquet su GCS via HTTPS (pattern compose).
--
-- Schema unificato:
--   data_elezione, tipo_elezione, regione, provincia, comune,
--   elettori, votanti, schede_bianche, affluenza_pct (calcolata),
--   lista, voti_lista, candidato, voti_candidato,
--   turno, seggi_lista, circoscrizione
--
-- Policy: ogni volta che un dataset sorgente pubblica un nuovo anno,
-- aggiungere l'URL alla lista corrispondente.

WITH

-- ── 1. Elezioni Comunali (2016-2024) ──────────────────────────────
comunali AS (
    SELECT
        data_elezione,
        'comunali' AS tipo_elezione,
        regione,
        provincia,
        comune,
        NULL AS circoscrizione,
        elettori,
        votanti,
        schede_bianche,
        ROUND(CAST(votanti AS DOUBLE) / NULLIF(CAST(elettori AS DOUBLE), 0) * 100, 2) AS affluenza_pct,
        lista,
        voti_lista,
        candidato,
        voti_candidato,
        turno,
        seggi_lista
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2016/elezioni_comunali_2016_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2017/elezioni_comunali_2017_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2018/elezioni_comunali_2018_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2019/elezioni_comunali_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2020/elezioni_comunali_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2021/elezioni_comunali_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_comunali/2024/elezioni_comunali_2024_clean.parquet'
    ], union_by_name=true)
),

-- ── 2. Elezioni Europee (1979-2024) ───────────────────────────────
europee AS (
    SELECT
        data_elezione,
        'europee' AS tipo_elezione,
        regione,
        provincia,
        comune,
        circoscrizione,
        elettori,
        votanti,
        schede_bianche,
        ROUND(CAST(votanti AS DOUBLE) / NULLIF(CAST(elettori AS DOUBLE), 0) * 100, 2) AS affluenza_pct,
        lista,
        voti_lista,
        NULL AS candidato,
        NULL AS voti_candidato,
        NULL AS turno,
        NULL AS seggi_lista
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/1979/elezioni_europee_1979_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/1984/elezioni_europee_1984_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/1989/elezioni_europee_1989_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/1994/elezioni_europee_1994_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/1999/elezioni_europee_1999_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2004/elezioni_europee_2004_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2009/elezioni_europee_2009_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2014/elezioni_europee_2014_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2019/elezioni_europee_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2024/elezioni_europee_2024_clean.parquet'
    ], union_by_name=true)
),

-- ── 3. Elezioni Regionali (2018-2024) ─────────────────────────────
regionali AS (
    SELECT
        data_elezione,
        'regionali' AS tipo_elezione,
        regione,
        provincia,
        comune,
        circoscrizione,
        elettori,
        votanti,
        schede_bianche,
        ROUND(CAST(votanti AS DOUBLE) / NULLIF(CAST(elettori AS DOUBLE), 0) * 100, 2) AS affluenza_pct,
        lista,
        voti_lista,
        candidato,
        voti_candidato,
        NULL AS turno,
        NULL AS seggi_lista
    FROM read_parquet([
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2018/elezioni_regionali_2018_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2019/elezioni_regionali_2019_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2020/elezioni_regionali_2020_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2021/elezioni_regionali_2021_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2023/elezioni_regionali_2023_clean.parquet',
        'https://storage.googleapis.com/dataciviclab-clean/elezioni_regionali/2024/elezioni_regionali_2024_clean.parquet'
    ], union_by_name=true)
)

-- ── Final: UNION ALL ──────────────────────────────────────────────
SELECT * FROM comunali
UNION ALL BY NAME
SELECT * FROM europee
UNION ALL BY NAME
SELECT * FROM regionali
