-- Mart: trend affluenza per tipo elezione × territorio
-- CAGR e variazione assoluta su finestre temporali
--
-- Colonne:
--   tipo_elezione, regione, provincia, comune,
--   primo_anno, ultimo_anno, anni_differenza, n_tornate,
--   prima_affluenza_pct, ultima_affluenza_pct,
--   cagr_affluenza_pct, var_assoluta_punti

WITH affluenza_comune AS (
    SELECT
        data_elezione,
        tipo_elezione,
        EXTRACT(YEAR FROM data_elezione) AS anno,
        regione,
        provincia,
        comune,
        AVG(CAST(votanti AS DOUBLE) / NULLIF(CAST(elettori AS DOUBLE), 0) * 100) AS affluenza_pct
    FROM clean_input
    GROUP BY data_elezione, tipo_elezione, regione, provincia, comune
),

-- Prima e ultima tornata per comune×tipo_elezione
anni_estremi AS (
    SELECT
        tipo_elezione,
        regione,
        provincia,
        comune,
        MIN(anno) AS primo_anno,
        MAX(anno) AS ultimo_anno,
        COUNT(DISTINCT anno) AS n_tornate
    FROM affluenza_comune
    GROUP BY tipo_elezione, regione, provincia, comune
),

-- Affluenza al primo anno
prima_affluenza AS (
    SELECT DISTINCT
        a.tipo_elezione,
        a.regione,
        a.provincia,
        a.comune,
        a.affluenza_pct AS prima_affluenza_pct
    FROM affluenza_comune a
    INNER JOIN anni_estremi e
        ON a.tipo_elezione = e.tipo_elezione
        AND a.regione = e.regione
        AND a.provincia = e.provincia
        AND a.comune = e.comune
        AND a.anno = e.primo_anno
),

-- Affluenza all'ultimo anno
ultima_affluenza AS (
    SELECT DISTINCT
        a.tipo_elezione,
        a.regione,
        a.provincia,
        a.comune,
        a.affluenza_pct AS ultima_affluenza_pct
    FROM affluenza_comune a
    INNER JOIN anni_estremi e
        ON a.tipo_elezione = e.tipo_elezione
        AND a.regione = e.regione
        AND a.provincia = e.provincia
        AND a.comune = e.comune
        AND a.anno = e.ultimo_anno
)

SELECT
    e.*,
    p.prima_affluenza_pct,
    u.ultima_affluenza_pct,
    -- CAGR: (ultima/prima)^(1/anni) - 1, in percentuale
    CASE
        WHEN p.prima_affluenza_pct > 0 AND e.ultimo_anno > e.primo_anno
        THEN ROUND(
            (POW(u.ultima_affluenza_pct / p.prima_affluenza_pct,
                  1.0 / (e.ultimo_anno - e.primo_anno)) - 1) * 100,
            2)
        ELSE NULL
    END AS cagr_affluenza_pct,
    -- Variazione assoluta in punti percentuali
    ROUND(u.ultima_affluenza_pct - p.prima_affluenza_pct, 2) AS var_assoluta_punti
FROM anni_estremi e
LEFT JOIN prima_affluenza p
    ON e.tipo_elezione = p.tipo_elezione
    AND e.regione = p.regione
    AND e.provincia = p.provincia
    AND e.comune = p.comune
LEFT JOIN ultima_affluenza u
    ON e.tipo_elezione = u.tipo_elezione
    AND e.regione = u.regione
    AND e.provincia = u.provincia
    AND e.comune = u.comune
ORDER BY cagr_affluenza_pct NULLS LAST, e.tipo_elezione, e.regione, e.provincia, e.comune
