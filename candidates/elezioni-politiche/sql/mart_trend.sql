-- Mart: trend affluenza elezioni politiche 1948-2022
-- Ogni riga: anno × camera_senato × circoscrizione

WITH affluenza AS (
    SELECT
        EXTRACT(YEAR FROM data_elezione) AS anno,
        camera_senato,
        circoscrizione,
        -- Affluenza media come % votanti su elettori
        AVG(CAST(votanti_totali AS DOUBLE) / NULLIF(CAST(elettori_totali AS DOUBLE), 0) * 100) AS affluenza_media_pct,
        SUM(votanti_totali) AS votanti_totali,
        SUM(elettori_totali) AS elettori_totali,
        COUNT(DISTINCT comune) AS comuni
    FROM clean_input
    WHERE elettori_totali > 0 AND votanti_totali > 0
    GROUP BY EXTRACT(YEAR FROM data_elezione), camera_senato, circoscrizione
),

-- Primo e ultimo anno per ogni circoscrizione
finestre AS (
    SELECT
        camera_senato,
        circoscrizione,
        MIN(anno) AS primo_anno,
        MAX(anno) AS ultimo_anno,
        MIN(affluenza_media_pct) FILTER (WHERE anno = (SELECT MIN(anno) FROM affluenza a2 WHERE a2.camera_senato = affluenza.camera_senato AND a2.circoscrizione = affluenza.circoscrizione)) AS prima_affluenza,
        MAX(affluenza_media_pct) FILTER (WHERE anno = (SELECT MAX(anno) FROM affluenza a2 WHERE a2.camera_senato = affluenza.camera_senato AND a2.circoscrizione = affluenza.circoscrizione)) AS ultima_affluenza
    FROM affluenza
    GROUP BY camera_senato, circoscrizione
)

SELECT
    a.anno,
    a.camera_senato,
    a.circoscrizione,
    ROUND(a.affluenza_media_pct, 2) AS affluenza_media_pct,
    a.votanti_totali,
    a.elettori_totali,
    a.comuni,
    -- Trend
    f.primo_anno,
    f.ultimo_anno,
    ROUND(f.prima_affluenza, 2) AS prima_affluenza_pct,
    ROUND(f.ultima_affluenza, 2) AS ultima_affluenza_pct,
    ROUND(f.ultima_affluenza - f.prima_affluenza, 2) AS var_assoluta_punti,
    -- CAGR
    CASE
        WHEN f.prima_affluenza > 0 AND (f.ultimo_anno - f.primo_anno) > 0
        THEN ROUND((POW(f.ultima_affluenza / NULLIF(f.prima_affluenza, 0), 1.0 / (f.ultimo_anno - f.primo_anno)) - 1) * 100, 2)
        ELSE NULL
    END AS cagr_annuale_pct
FROM affluenza a
LEFT JOIN finestre f ON a.camera_senato = f.camera_senato AND a.circoscrizione = f.circoscrizione
ORDER BY a.camera_senato, a.circoscrizione, a.anno
